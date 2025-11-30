from django.urls import path
from . import views
from .views import DashboardPageView, UsersPageView, AddUsersStaffView
from gamification.views import StaffGamificationView
from gamification.views import TaskCreateView, UserTaskCreateView, ConquistaCreateView # CREATE
from tenants.views import StaffTenantView
from accounts.views import UserStaffDeleteView, UserStaffEditView

urlpatterns = [
    path('dashboard/', DashboardPageView.as_view(), name='dashboard_staff'),
    path('users/', UsersPageView.as_view(), name='users_staff'),
    path('users/add/', AddUsersStaffView.as_view(), name='add_users_staff'), 
    path('users/delete/<int:pk>/', UserStaffDeleteView.as_view(), name='delete_user_staff'),
    path('users/edit/<int:pk>/', UserStaffEditView.as_view(), name='edit_user_staff'),
    path('game/', StaffGamificationView.as_view(), name='game_staff'), 
    path('game/task/novo/', TaskCreateView.as_view(), name='task_create'),  
    path('game/usertask/novo/', UserTaskCreateView.as_view(), name='user_task_create'), 
    path('game/conquista/novo/', ConquistaCreateView.as_view(), name='conquista_create'),
    path('tenant/', StaffTenantView.as_view(), name='tenant_staff'),
]
