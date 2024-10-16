from django.contrib import admin
from django.urls import path
from . import views
from .API import *


urlpatterns = [
    # path('login/', views.login, name='login'),

    #API
    path('register', register_user, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('newuseraip',newuserapi, name='newuserapi'),
    # path('details/<str:id>', user_details, name='user_details'),
    path('details', user_details, name='user_details'),

]