from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Tenant
from accounts.models import User
from .forms import TenantForm
from accounts.forms import UserFormTenant
from django.urls import reverse_lazy

class TenantCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'tenants/tenants_form.html'
    success_url = reverse_lazy('tenant_list')
    
    def test_func(self):
        user = self.request.user
        return user.is_superuser

class TenantListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Tenant
    template_name = 'tenants/tenants_list.html'
    context_object_name = 'tenants'
        
    def test_func(self):
        user = self.request.user
        return user.is_superuser

class TenantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'tenants/tenants_form.html'
    success_url = reverse_lazy('tenant_list')
    
    def test_func(self):
        user = self.request.user
        return user.is_superuser

class TenantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tenant
    template_name = 'tenants/tenants_delete.html'
    success_url = reverse_lazy('tenant_list')
    
    def test_func(self):
        user = self.request.user
        return user.is_superuser
    
class TenantListUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'tenants/tenants_users.html'
    context_object_name = 'users'

    def test_func(self):
        user = self.request.user
        tenant_id = self.kwargs["pk"]
        return user.is_superuser or (user.is_staff and user.tenant_id == int(tenant_id))
    
    def get_queryset(self):
        tenant_id = self.kwargs["pk"]
        return User.objects.filter(tenant_id=tenant_id)

# CLASS PARA CRIAR UM USUARIO QUANDO VC ESTA DENTRO DE UM TENANT
class TenantCreateUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserFormTenant
    template_name = "tenants/tenants_form.html"
    
    def test_func(self):
        user = self.request.user
        tenant_id = self.kwargs["pk"]
        return user.is_superuser or (user.is_staff and user.tenant_id == int(tenant_id))
    
    def form_valid(self, form):
    
        tenant_id = self.kwargs['pk']    
        self.object = form.save(commit=False) 
        self.object.tenant_id = tenant_id
        self.object.save()
        return super().form_valid(form) 
    
    def get_success_url(self):
        tenant_id = self.kwargs["pk"]
        return reverse_lazy('tenant_users', kwargs={'pk': tenant_id})