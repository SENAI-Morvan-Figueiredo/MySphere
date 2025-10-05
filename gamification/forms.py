from django import forms
from .models import Task, User_Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descricao', 'pontos']
        
class UserTaskForm(forms.ModelForm):
    class Meta:
        model = User_Task
        fields = ['user', 'task']