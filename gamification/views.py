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

class TaskListView(OnlyIsStaff, TenantAccessMixin, ListView):
    model = Task
    template_name = 'gamification/gamification_tasks_list.html'
    context_object_name = 'tasks'

class UserTaskListView(OnlyIsStaff, TenantAccessMixin, ListView):
    model = User_Task
    template_name = 'gamification/gamification_users_tasks_list.html'
    context_object_name = 'user_tasks'

class PointsListView(OnlyIsStaff, TenantAccessMixin, ListView):
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

# VIEW PARA CRIAR O RANKING GAMIFICATION

@login_required
def game_ranking(request, tenant_id=None):
   
    tenant_id = tenant_id or getattr(request.user, 'tenant_id', None)

    if not tenant_id:
        return render(request, "gamification/error.html", {"mensagem": "Tenant não identificado."})

    ranking = Points.objects.filter(
        tenant_id=tenant_id
    ).annotate(
        posicao=Window(
            expression=RowNumber(),
            order_by=F('pontos').desc()
        )
    ).order_by('-pontos')

    top5 = ranking[:5]

    user_line = ranking.filter(user=request.user).first()

    return render(request, "gamification/gamification_points_user.html", {
        "top5": top5,
        "user_line": user_line,
        "tenant_id": tenant_id,
    })


# VIEWS - CREATE

class TaskCreateView(OnlyIsStaff, TenantAccessMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "gamification/gamification_tasks_form.html"
    success_url = reverse_lazy('task_list')
    
class UserTaskCreateView(OnlyIsStaff, TenantAccessMixin, CreateView):
    model = User_Task
    form_class = UserTaskForm
    template_name = "gamification/gamification_users_tasks_form.html"
    success_url = reverse_lazy('user_task_list')

    def form_valid(self, form):
        form.instance.atribuido_por = self.request.user 
        return super().form_valid(form)

# VIEWS - UPDATE 

class TaskUpdateView(OnlyIsStaff, TenantAccessMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'gamification/gamification_tasks_form.html'
    success_url = reverse_lazy('task_list')

class UserTaskUpdateView(OnlyIsStaff, TenantAccessMixin, UpdateView):
    model = User_Task
    form_class = UserTaskForm
    template_name = 'gamification/gamification_users_tasks_form.html'
    success_url = reverse_lazy('user_task_list')

# VIEWS - DELETE 

class TaskDeleteView(OnlyIsStaff, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')

class UserTaskDeleteView(OnlyIsStaff, DeleteView):
    model = User_Task
    success_url = reverse_lazy('user_task_list')