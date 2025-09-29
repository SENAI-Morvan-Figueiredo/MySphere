from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import User
from .forms import UserForm
from django.urls import reverse_lazy
# Create your views here.


class Users(ListView):
    model = User
    template_name = "accounts/account_list.html"
    context_object_name = "users"

class novo(CreateView):
    model = User
    form_class = UserForm
    template_name = "accounts/add.html"
    success_url = reverse_lazy('users')