from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Task, User_Task, Points, Conquista, User_Conquista
from .forms import TaskForm, UserTaskForm, ConquistaForm
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
        context['conquistas'] = Conquista.objects.filter(tenant=tenant)

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
                    order_by=F('points_total').desc()

                )
            ).order_by('-points_total')

            top5 = ranking[:5]
            user_line = ranking.filter(user=user).first()
            context['ranking'] = top5
            context['user_line'] = user_line

        ranking_geral = Points.objects.annotate(
            posicao=Window(
                expression=RowNumber(),
                order_by=F('points_total').desc()
            )
        ).order_by('-points_total')

        top10_geral = ranking_geral[:5]  
        user_line_geral = ranking_geral.filter(user=user).first()

        context['ranking_geral'] = top10_geral
        context['user_line_geral'] = user_line_geral

        context['user_tasks'] = User_Task.objects.filter(user=user)
        context['conquistas'] = User_Conquista.objects.filter(user=user)

        return context

@require_POST
@login_required
def concluir_tarefa(request, task_id):
    user_task = get_object_or_404(User_Task, id=task_id, user=request.user)

    if user_task.concluido:
        return redirect('game_home')

    user_task.concluido = True
    user_task.save()

    pontos_user, created = Points.objects.get_or_create(
        user=request.user,
        defaults={
            'tenant': request.user.tenant,
            'points_atual': 0,
            'points_total': 0,
            'nivel': 'Iniciante'
        }
    )

    if user_task.task.pontos > 0:
        pontos_user.add_points(user_task.task.pontos)

    if user_task.task.conquista:
        User_Conquista.objects.get_or_create(
            user=request.user,
            conquista=user_task.task.conquista
        )

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

# CONQUISTAS

class ConquistaListView(ListView):
    model = Conquista
    template_name = "gamification/gamification_points_user.html"
    context_object_name = "conquistas"

class ConquistaCreateView(OnlyIsStaff, TenantAccessMixin, CreateView):
    model = Conquista
    form_class = ConquistaForm
    template_name = "gamification/gamification_conquista_form.html"
    success_url = reverse_lazy('game_staff')

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)

class ConquistaUpdateView(OnlyIsStaff, TenantAccessMixin, UpdateView):
    model = Conquista
    form_class = ConquistaForm
    template_name = "gamification/gamification_conquista_form.html"
    success_url = reverse_lazy('game_staff')

class ConquistaDeleteView(OnlyIsStaff, DeleteView):
    model = Conquista
    success_url = reverse_lazy('game_staff')
