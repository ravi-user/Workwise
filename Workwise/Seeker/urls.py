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
    path('s-profile/', views.s_profile, name='s-profile'),
    path('change-pass/', views.change_pass, name='change-pass'),
    path('change-img/', views.change_img, name='change-img'),
    path('social-media/', views.social_media, name='social-media'),
    path('add-link/',views.add_link,name='add-link'),

    path('s-all-project/', views.s_all_projects, name='s-all-project'),
    path('s-all-job/', views.s_all_job, name='s-all-job'),
    path('saveproject/', views.save_project, name='saveproject'), 
    path('savedproject/', views.saved_project, name='savedproject'),
    path('projectlike', views.project_like, name='projectlike'),
    path('pslike/', views.ps_like, name='pslike'),
    path('savejob/', views.save_job, name='savejob'),
    path('joblike', views.job_like, name='joblike'),
    path('js-like/',views.js_like, name='js-like'),
    path('savedjob/', views.saved_job, name='savedjob'),
    path('save-all-jobs/', views.save_all_job , name='save-all-jobs'),
    path('apply-jobs/', views.apply_job , name='apply-jobs'),
    path('save-apply-job/',views.save_apply_job, name='save-apply-job'),
    path('save_all_project/', views.save_all_project, name='save_all_project'),
    path('bid-project/', views.bid_project, name='bid-project'),
    path('bid-sproject/', views.bid_sproject, name='bid-sproject'),

    path('com-all/', views.com_all, name='com-all'),
    path('search/',views.search,name='search'),

    path('p-comment/',views.p_comment,name='p-comment'),
    path('send-comm/',views.send_comm,name='send-comm'),
    path('ps-comment/',views.ps_comment, name='ps-comment'),
    path('ps-send-com/',views.ps_send_com,name='ps-send-com'),
    path('j-comment/',views.j_comment,name='j-comment'),
    path('j-send-comment/',views.j_send_comment,name='j-send-comment'),

    path('notification/',views.notification,name='notification'),
    path('c-follow/', views.c_follow, name='c-follow'),
    path('del-account/', views.del_account, name='del-account'),
    path('page/',views.page, name='page'),
    
]
