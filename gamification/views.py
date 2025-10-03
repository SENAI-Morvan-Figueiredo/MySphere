from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Task, User_Task, Points
from .forms import TaskForm, UserTaskForm

# VIEWS - LIST

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

# VIEWS - CREATE

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "gamification/gamification_tasks_form.html"
    success_url = reverse_lazy('task_list')
    
class UserTaskCreateView(CreateView):
    model = User_Task
    form_class = UserTaskForm
    template_name = "gamification/gamification_users_tasks_form.html"
    success_url = reverse_lazy('user_task_list')
