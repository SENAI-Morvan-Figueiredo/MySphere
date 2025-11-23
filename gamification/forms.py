from django import forms
from .models import Task, User_Task, Conquista

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descricao', 'pontos', 'conquista']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'pontos': forms.NumberInput(attrs={'class': 'form-control'}),
            'conquista': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'pontos': 'Pontos da Task',
            'conquista': 'Conquista concedida (opcional)'
        }

        
class UserTaskForm(forms.ModelForm):
    class Meta:
        model = User_Task
        fields = ['user', 'task']

class ConquistaForm(forms.ModelForm):
    class Meta:
        model = Conquista
        fields = ['nome', 'descricao', 'imagem']
