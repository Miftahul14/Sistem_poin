from django.urls import path
from .import views

urlpatterns = [
    path('', views.HalamanLogin, name='HalamanLogin'),
    path('HalamanLogout/', views.HalamanLogout, name='HalamanLogout'),
]