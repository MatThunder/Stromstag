from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='test-home'),
    path('home/', views.home, name='test-home'),
    path('home-new/', views.homeNew, name='neuesHome'),
    path('about/', views.about, name='test-about'),
    path('chart/', views.chart, name='chart'),

]