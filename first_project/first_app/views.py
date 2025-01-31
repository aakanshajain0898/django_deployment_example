from django.shortcuts import render
from django.http import HttpResponse
from first_app.models import AccessRecord,Topic,WebPage
# from first_app.models import Users
# from . import forms
from first_app.forms import NewUserForm
from first_app.forms import UserForm,UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request) :
    #return HttpResponse("<em>Hello World!</em>")
    # my_dict={'insert_me':"Hello I am from view.py !"}
    my_dict={'insert_me':"Now I am comming from first_app/index.html!",'text':'Hello world!','number':100}
    return render(request,'first_app/index.html',context=my_dict)

    # webpages_list=AccessRecord.objects.order_by('date')
    # date_dict={'access_records':webpages_list}
    # return render(request,'first_app/index.html',context=access_records)

@login_required
def user_logout(request) :
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request) :
    return HttpResponse("You are logged in, Nice!")

def register(request) :
    registered=False

    if request.method=="POST" :
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() :
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES :
                profile.profile_pic=request.FILES['profile_pic']


            profile.save()
            registered=True
        else :
            print(user_form.errors,profile_form.errors)
    else :
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
    return render(request,'first_app/registration.html',context=
                                                                {'user_form':user_form,
                                                                'profile_form':profile_form,
                                                                'registered':registered})

def user_login(request) :
    if request.method=="POST" :
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)

        if user :
            if user.is_active :
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else :
                return HttpResponse("Account not active!")
        else:
            print("Someone tried tologin and failed!")
            print("Username: {} and Password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied!")
    else :
        return render(request,'first_app/login.html',{})

def other(request) :
    return render(request,'first_app/other.html')

def relative(request) :
    return render(request,'first_app/relative_url_templates.html')

def help(request) :
    help_dict={'help_insert':"Help Page !"}
    return render(request,'first_app/help.html',context=help_dict)

def users(request) :
    user_list=User.objects.order_by('first_name')
    user_dict={'users':user_list}
    return render(request,'first_app/users.html',context=user_dict)

def signup_form(request) :
    form=NewUserForm()

    if request.method=="POST" :
        form=NewUserForm(request.POST)

        if form.is_valid() :
            form.save(commit=True)
            return index(request)
        else :
            print('Error from invalid')
    return render(request,'first_app/form_page.html',context={'form':form})

def form_name_view(request) :
    form=forms.FormName()

    if request.method=='POST':
        form=forms.FormName(request.POST)

        if form.is_valid() :
            # Do somthing code
            print("Validation Success!")
            print("Name: "+form.cleaned_data['name'])
            print("Email: "+form.cleaned_data['email'])
            print("Text: "+form.cleaned_data['text'])
    return render(request,'first_app/form_page.html',context={'form':form})
