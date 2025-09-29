from django.urls import path
from .views import TenantCreateView, TenantListView, TenantUpdateView, TenantDeleteView

urlpatterns = [
    path('lista/', TenantListView.as_view(), name='tenant_list'),
    path('excluir/<int:pk>', TenantDeleteView.as_view(), name='tenant_delete'),
    path('criar/', TenantCreateView.as_view(), name='tenant_create'),
    path('edit/<int:pk>', TenantUpdateView.as_view(), name='tenant_edit'),
]