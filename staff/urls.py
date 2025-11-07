from django.urls import path
from . import views
from .views import DashboardPageView, UsersPageView #, AddUsersStaffView
from gamification.views import StaffGamificationView

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home_staff'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard_staff'),
    path('users/', UsersPageView.as_view(), name='users_staff'),
    # path('users/add/', AddUsersStaffView.as_view(), name='add_users_staff'), # AJUSTES A FAZER MAS FUNCIONA,
    path('game/', StaffGamificationView.as_view(), name='game_staff') # provisorio
]
