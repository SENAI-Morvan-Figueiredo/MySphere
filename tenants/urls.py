from django.urls import path
from .views import TenantCreateView, TenantListView, TenantUpdateView, TenantDeleteView, TenantListUsersView, TenantCreateUserView, TenantUpdateUserView, TenantDeleteUserView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TenantListView.as_view(), name='tenant_list'), 
    path('criar/', TenantCreateView.as_view(), name='tenant_create'), 
    path('edit/<int:pk>', TenantUpdateView.as_view(), name='tenant_edit'), 
    path('<int:pk>/delete/', TenantDeleteView.as_view(), name='tenant_delete'), 
    path('<int:pk>/users/', TenantListUsersView.as_view(), name=('tenant_users')), 
    path('<int:pk>/users/add/', TenantCreateUserView.as_view(), name=('tenant_users_create')), 
    path('<int:tenant_pk>/users/<int:pk>/edit/', TenantUpdateUserView.as_view(), name='tenant_users_edit'),
    path('<int:tenant_pk>/users/<int:pk>/delete/', TenantDeleteUserView.as_view(), name='tenant_users_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)