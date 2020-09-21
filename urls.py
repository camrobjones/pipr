"""Pronouns URLs"""
from django.urls import path

from pronouns import views


urlpatterns = [
    path('', views.home),
    path('expt', views.expt),
    path('save_results/', views.save_results),
    path('validate_captcha/', views.validate_captcha),
    path('error', views.error),
]
