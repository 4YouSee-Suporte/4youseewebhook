from django.urls import path

from webhook.base import views

urlpatterns = [
    path('', views.home, name='home'),
]