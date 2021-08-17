from django.urls import path

from webhook.manager import views

app_name = 'manager'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:slug>/', views.conta, name='conta'),

    # Atualiza os recusos da conta
    path(r'update/<slug:slug>/all', views.update_all_data_account, name='update_data_account'),
    path(r'update/<slug:slug>/categories/', views.update_categories, name='update_categories'),
    path(r'update/<slug:slug>/medias/', views.update_medias, name='update_medias'),
    path(r'update/<slug:slug>/players/', views.update_players, name='update_players'),
    path(r'update/<slug:slug>/playlists/', views.update_playlists, name='update_playlists'),
    path(r'update/<slug:slug>/playlists/', views.update_playlists, name='update_playlists'),

    # Deleta conta(s)
    path(r'delete/<slug:slug>/', views.delete, name='delete'),
]
