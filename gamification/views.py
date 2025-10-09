from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Task, User_Task, Points
from .forms import TaskForm, UserTaskForm
from .mixins import TenantAccessMixin

# VIEWS - LIST

class TaskListView(TenantAccessMixin, ListView):
    model = Task
    template_name = 'gamification/gamification_tasks_list.html'
    context_object_name = 'tasks'

class UserTaskListView(TenantAccessMixin, ListView):
    model = User_Task
    template_name = 'gamification/gamification_users_tasks_list.html'
    context_object_name = 'user_tasks'

class PointsListView(TenantAccessMixin, ListView):
    model = Points
    template_name = 'gamification/gamification_points_list.html'
    context_object_name = 'points'

# VIEW QUE RENDERIZA PONTOS E TASKS DO USER

class GameHomeView(ListView):
    model = Points
    template_name = 'gamification/gamification_points_user.html'
    context_object_name = 'points'

    def get_queryset(self):
        user = self.request.user
        return Points.objects.filter(user=user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_tasks'] = User_Task.objects.filter(user=self.request.user)
        return context

# VIEWS - CREATE

class TaskCreateView(TenantAccessMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "gamification/gamification_tasks_form.html"
    success_url = reverse_lazy('task_list')
    
class UserTaskCreateView(TenantAccessMixin, CreateView):
    model = User_Task
    form_class = UserTaskForm
    template_name = "gamification/gamification_users_tasks_form.html"
    success_url = reverse_lazy('user_task_list')

    def form_valid(self, form):
        form.instance.atribuido_por = self.request.user 
        return super().form_valid(form)

# VIEWS - UPDATE 

class TaskUpdateView(TenantAccessMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'gamification/gamification_tasks_form.html'
    success_url = reverse_lazy('task_list')

class UserTaskUpdateView(TenantAccessMixin, UpdateView):
    model = User_Task
    form_class = UserTaskForm
    template_name = 'gamification/gamification_users_tasks_form.html'
    success_url = reverse_lazy('user_task_list')

# VIEWS - DELETE 

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')

class UserTaskDeleteView(DeleteView):
    model = User_Task
    success_url = reverse_lazy('user_task_list')