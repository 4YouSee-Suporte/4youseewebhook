from django.urls import path

from webhook.base import views

app_name = 'base'

urlpatterns = [
    path('', views.home, name='home'),
]
