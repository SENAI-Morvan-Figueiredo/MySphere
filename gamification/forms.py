from django import forms
from .models import Task, User_Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descricao', 'pontos', 'criado_por', 'tenant']
        
class UserTaskForm(forms.ModelForm):
    class Meta:
        model = User_Task
        fields = ['user', 'task', 'atribuido_por', 'concluido', 'concluido_em']