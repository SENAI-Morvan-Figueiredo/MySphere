from django.urls import path
from .views import TenantCreateView, TenantListView, TenantUpdateView, TenantDeleteView, TenantListUsersView, TenantCreateUserView

urlpatterns = [
    path('lista/', TenantListView.as_view(), name='tenant_list'),
    path('criar/', TenantCreateView.as_view(), name='tenant_create'),
    path('edit/<int:pk>', TenantUpdateView.as_view(), name='tenant_edit'),
    path('lista/<int:pk>/delete/', TenantDeleteView.as_view(), name='tenant_delete'),
    path('lista/<int:pk>/users/', TenantListUsersView.as_view(), name=('tenant_users')),
    path('lista/<int:pk>/users/add/', TenantCreateUserView.as_view(), name=('tenant_users_create')),
]