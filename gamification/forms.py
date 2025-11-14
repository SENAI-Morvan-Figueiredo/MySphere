from django import forms
from .models import Task, User_Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descricao', 'pontos']
        
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Completar relatório mensal'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Forneça uma breve descrição dos requisitos da tarefa...',
                'rows': 3
            }),
            'pontos': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 100'
            }),
        }
        labels = {
            'titulo': 'Título da Tarefa',
            'descricao': 'Descrição',
            'pontos': 'Pontos'
        }
        
class UserTaskForm(forms.ModelForm):
    class Meta:
        model = User_Task
        fields = ['user', 'task']