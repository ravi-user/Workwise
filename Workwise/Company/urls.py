"""Workwise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('',views.sign_in, name='sign-in'),
    path('index/', views.index , name='index'),
    path('profile/', views.profile , name='profile'),
    path('logout/', views.logout, name='logout'),
    path('add-jobs/', views.add_jobs, name='add-jobs'),
    path('my-jobs/', views.my_jobs, name='my-jobs'),
    path('all-jobs/', views.all_jobs, name='all-jobs'),
    path('add-project', views.add_project, name='add-project'),
    path('my-project/', views.my_project, name='my-project'),
    path('all-project/', views.all_project, name='all-project'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('otp/', views.otp, name='otp'),
    path('reset-passsword/', views.reset_password, name='reset-password'),

    path('proj-com/',views.proj_com,name='proj-com'),
    path('job-com/',views.job_com,name='job-com'),
    path('c-social-link/',views.c_social_link,name='c-social-link'),
    path('c-add-link/',views.c_add_link,name='c-add-link'),
    path('c-change-pass/',views.c_change_pass,name='c-change-pass'),
    path('c-change-img/',views.c_change_img,name='c-change-img'),
    path('c-notification/',views.c_notification,name='c-notification'),



]
