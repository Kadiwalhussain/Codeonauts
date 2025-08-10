from django.urls import path
from . import views

app_name = 'apod'

urlpatterns = [
    path('', views.apod_home, name='home'),
    path('archive/', views.apod_archive, name='archive'),
    path('detail/<str:date>/', views.apod_detail, name='detail'),
    path('refresh/', views.refresh_apod, name='refresh'),
] 