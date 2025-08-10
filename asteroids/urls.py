from django.urls import path
from . import views

app_name = 'asteroids'

urlpatterns = [
    path('', views.asteroids_home, name='home'),
    path('list/', views.asteroids_list, name='list'),
    path('approaches/', views.approaches_list, name='approaches'),
    path('refresh/', views.refresh_asteroids, name='refresh'),
] 