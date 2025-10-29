from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from accounts.models import User

def error_403_view(request, exception=None):
    return render(request, 'staff/403.html', status=403)

class HomePageView(TemplateView):
    template_name = 'staff/home.html'

class DashboardPageView(TemplateView):
    template_name = 'staff/dashboard.html'
    
class UsersPageView(ListView):
    model = User
    template_name = 'staff/users.html'
    context_object_name = 'users'