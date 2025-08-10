from django.urls import path
from . import views

app_name = 'solarflares'

urlpatterns = [
    path('', views.solar_flares_home, name='home'),
    path('list/', views.solar_flares_list, name='list'),
    path('refresh/', views.refresh_solar_flares, name='refresh'),
] 