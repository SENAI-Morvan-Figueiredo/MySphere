from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import Task, User_Task, Points

# Create your views here.

class TaskListView(ListView):
    model = Task
    template_name = 'gamification/gamification_tasks_list.html'
    context_object_name = 'tasks'

class UserTaskListView(ListView):
    model = User_Task
    template_name = 'gamification/gamification_users_tasks_list.html'
    context_object_name = 'user_tasks'

class PointsListView(ListView):
    model = Points
    template_name = 'gamification/gamification_points_list.html'
    context_object_name = 'points'