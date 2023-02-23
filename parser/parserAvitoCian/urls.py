from django.contrib import admin
from django.urls import path, include
from . import views
from .views import request_proceed

urlpatterns = [
    path('', views.all_Advertisment),
    path('request_proceed/', request_proceed, name='request_proceed')
]