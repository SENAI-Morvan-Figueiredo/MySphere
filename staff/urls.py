from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_staff'),
    path('dashboard/', views.DashboardPageView.as_view(), name='dashboard_staff'),
    path('users/', views.UsersPageView.as_view(), name='users_staff')
]
