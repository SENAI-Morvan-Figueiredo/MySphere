from django.urls import path
from .views import TenantCreateView, TenantListView

urlpatterns = [
    path('lista/', TenantListView.as_view(), name='tenant_list'),
    path('criar/', TenantCreateView.as_view(), name='tenant_create'),
]