from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Tenant
from accounts.models import User
from .forms import TenantForm#, TenantStaffForm
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant_id = self.kwargs["pk"]
        context['tenant'] = Tenant.objects.get(pk=tenant_id)
        return context

# CLASS PARA CRIAR UM USUARIO QUANDO VC ESTA DENTRO DE UM TENANT
class TenantCreateUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserFormTenant
    template_name = "tenants/tenants_user_form.html"
    
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

class TenantUpdateUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserFormTenant
    template_name = "tenants/tenants_user_form.html"

    def test_func(self):
        user = self.request.user
        tenant_id = self.kwargs["tenant_pk"]
        return user.is_superuser or (user.is_staff and user.tenant_id == int(tenant_id))

    def get_success_url(self):
        return reverse_lazy('tenant_users', kwargs={'pk': self.kwargs["tenant_pk"]})

class TenantDeleteUserView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "tenants/tenants_delete_user.html"

    def test_func(self):
        user = self.request.user
        tenant_id = self.kwargs["tenant_pk"]
        return user.is_superuser or (user.is_staff and user.tenant_id == int(tenant_id))

    def get_success_url(self):
        return reverse_lazy('tenant_users', kwargs={'pk': self.kwargs["tenant_pk"]})


# CLASS PARA TELA DE STAFF

class StaffTenantView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'staff/staff_tenant.html'
    success_url = reverse_lazy('tenant_staff')

    def test_func(self):
        return self.request.user.is_staff 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = Tenant.objects.get(pk=self.request.user.tenant.pk)
        context["tenant"] = tenant
        context["form"] = TenantForm(instance=tenant)
        context["modoForm"] = self.request.GET.get("edit") == "true"
        return context

    def post(self, request, *args, **kwargs):
        tenant = Tenant.objects.get(pk=self.request.user.tenant.pk)
        form = TenantForm(request.POST, request.FILES, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        context = self.get_context_data()
        context["form"] = form
        context["modoForm"] = True
        return self.render_to_response(context)