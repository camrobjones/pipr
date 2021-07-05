"""Pronouns URLs"""
from django.urls import path

from pipr3 import views


urlpatterns = [
    path('control', views.home),
    path('expt', views.expt),
    path('save_results/', views.save_results),
    path('validate_captcha/', views.validate_captcha),
    path('ua_data/', views.ua_data),
    path('error', views.error),
    path('data/<str:model>/', views.download_data),
]
