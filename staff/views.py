from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from accounts.models import User
from .forms import FormAddUsersStaff
from django.urls import reverse_lazy
from .mixins import StaffRequiredMixin

def error_403_view(request, exception=None):
    return render(request, 'staff/403.html', status=403)

class HomePageView(StaffRequiredMixin, TemplateView):
    template_name = 'staff/staff_home.html'

class DashboardPageView(StaffRequiredMixin, TemplateView):
    template_name = 'staff/staff_dashboard.html'
    
# class UsersPageView(ListView):
#     model = User
#     template_name = 'staff/users.html'
#     context_object_name = 'users'

#     def get_queryset(self):
#         tenant_id = self.request.user.tenant.pk
#         return User.objects.filter(tenant_id=tenant_id)

class AddUsersStaffView(CreateView):
    model = User
    form_class = FormAddUsersStaff
    template_name = "staff/users.html"
    success_url = reverse_lazy('users_staff')

    def form_valid(self, form):
        tenant_id = self.request.user.tenant.pk
        self.object = form.save(commit=False) 
        self.object.tenant_id = tenant_id
        self.object.save()
        return super().form_valid(form) 

class UsersPageView(StaffRequiredMixin, TemplateView):
    template_name = "staff/staff_users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = FormAddUsersStaff()
        context["users"] = User.objects.filter(tenant=self.request.user.tenant)
        return context

    def post(self, request, *args, **kwargs):
            form = FormAddUsersStaff(request.POST, request.FILES)
            if form.is_valid():
                new_user = form.save(commit=False)
                new_user.tenant = request.user.tenant
                new_user.save()
                return redirect("users_staff") 
            
            context = self.get_context_data()
            context["form"] = form
            
            return self.render_to_response(context)