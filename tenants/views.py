from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Tenant
from .forms import TenantForm
from django.urls import reverse_lazy

class TenantCreateView(CreateView):
    model = Tenant
    form_class = TenantForm
    template_name = 'tenants/tenants_form.html'
    success_url = reverse_lazy('tenant_list')

class TenantListView(ListView):
    model = Tenant
    template_name = 'tenants/tenants_list.html'
    context_object_name = 'tenants'