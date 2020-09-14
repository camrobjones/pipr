"""Pronouns URLs"""
import logging

from django.urls import path

logger = logging.getLogger('django')
logger.info("Loading pronouns...")

from pronouns import views


urlpatterns = [
    path('', views.home),
    path('expt', views.expt),
    path('save_results/', views.save_results),
]
