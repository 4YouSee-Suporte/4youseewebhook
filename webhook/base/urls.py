from django.urls import path

from webhook.base import views

app_name = 'base'

urlpatterns = [
    path('playlogs/', views.playlogs, name='playlogs'),
    path('relatorio/', views.solicitar_relatorio, name='solicitar_relatorio')
]
