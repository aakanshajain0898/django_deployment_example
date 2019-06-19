from django.urls import path
from django.conf.urls import url
from first_app import views

#Template tagging
app_name='first_app'

urlpatterns = [
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^relative/$',views.relative,name='relative'),
    url(r'^other/$',views.other,name='other'),
    #path('',views.index,name='index'),
    #path('',views.help,name='help'),
    path('',views.users,name='users'),
]
