from django.shortcuts import render
from django.views.generic import TemplateView

def error_403_view(request, exception=None):
    return render(request, 'staff/403.html', status=403)

class HomePageView(TemplateView):
    template_name = 'staff/home.html'