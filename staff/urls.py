from django.urls import path
from . import views
from .views import DashboardPageView, UsersPageView #, AddUsersStaffView

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_staff'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard_staff'),
    path('users/', UsersPageView.as_view(), name='users_staff'),
    # path('users/add/', AddUsersStaffView.as_view(), name='add_users_staff'),
]
