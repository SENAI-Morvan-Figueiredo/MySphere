from django.urls import path
from .views import TenantCreateView, TenantListView, TenantUpdateView, TenantDeleteView, TenantListUsersView, TenantCreateUserView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TenantListView.as_view(), name='tenant_list'), 
    path('criar/', TenantCreateView.as_view(), name='tenant_create'), 
    path('edit/<int:pk>', TenantUpdateView.as_view(), name='tenant_edit'), 
    path('lista/<int:pk>/delete/', TenantDeleteView.as_view(), name='tenant_delete'), 
    path('lista/<int:pk>/users/', TenantListUsersView.as_view(), name=('tenant_users')), # STAFF
    path('lista/<int:pk>/users/add/', TenantCreateUserView.as_view(), name=('tenant_users_create')), # STAFF
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)