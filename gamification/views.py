from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Task, User_Task, Points
from .forms import TaskForm, UserTaskForm
from .mixins import TenantAccessMixin, OnlyIsStaff
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import F, Window
from django.db.models.functions import RowNumber

# VIEWS - LIST

class StaffGamificationView(OnlyIsStaff, TenantAccessMixin, ListView):
    template_name = 'staff/staff_gamification.html'
    model = Points
    context_object_name = 'points'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tenant = self.request.user.tenant
        context['tasks'] = Task.objects.filter(tenant=tenant)
        context['user_tasks'] = User_Task.objects.filter(task__tenant=tenant)

        return context


# VIEW QUE RENDERIZA PONTOS E TASKS DO USER

class GameHomeView(OnlyIsStaff, TenantAccessMixin, ListView):
    model = Points
    template_name = 'gamification/gamification_points_user.html'
    context_object_name = 'points'

    def get_queryset(self):
        user = self.request.user
        return Points.objects.filter(user=user)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        tenant_id = getattr(user, 'tenant_id', None)

        if tenant_id:
            ranking = Points.objects.filter(
                tenant_id=tenant_id
            ).annotate(
                posicao=Window(
                    expression=RowNumber(),
                    order_by=F('pontos').desc()
                )
            ).order_by('-pontos')

            top5 = ranking[:5]
            user_line = ranking.filter(user=user).first()
            context['ranking'] = top5
            context['user_line'] = user_line

        context['user_tasks'] = User_Task.objects.filter(user=user)

        return context

@require_POST
@login_required
def concluir_tarefa(request, task_id):
    user_task = get_object_or_404(User_Task, id=task_id, user=request.user)

    if not user_task.concluido:
        user_task.concluido = True
        user_task.save()
        
    pontos_user = Points.objects.get(user=request.user)
    pontos_user.save()
    pontos_user.atualizar_nivel()
    
    return redirect('game_home')

# VIEWS - CREATE

class TaskCreateView(OnlyIsStaff, TenantAccessMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "gamification/gamification_tasks_form.html"
    success_url = reverse_lazy('game_staff')
    
class UserTaskCreateView(OnlyIsStaff, TenantAccessMixin, CreateView):
    model = User_Task
    form_class = UserTaskForm
    template_name = "gamification/gamification_users_tasks_form.html"
    success_url = reverse_lazy('game_staff')

    def form_valid(self, form):
        form.instance.atribuido_por = self.request.user 
        return super().form_valid(form)

# VIEWS - UPDATE 

class TaskUpdateView(OnlyIsStaff, TenantAccessMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'gamification/gamification_tasks_form.html'
    success_url = reverse_lazy('game_staff')

class UserTaskUpdateView(OnlyIsStaff, TenantAccessMixin, UpdateView):
    model = User_Task
    form_class = UserTaskForm
    template_name = 'gamification/gamification_users_tasks_form.html'
    success_url = reverse_lazy('game_staff')

# VIEWS - DELETE 

class TaskDeleteView(OnlyIsStaff, DeleteView):
    model = Task
    success_url = reverse_lazy('game_staff')

class UserTaskDeleteView(OnlyIsStaff, DeleteView):
    model = User_Task
    success_url = reverse_lazy('game_staff')