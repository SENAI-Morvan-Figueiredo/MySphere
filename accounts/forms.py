from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nome', 'email', 'senha', 'foto', 'data_nascimento', 'tenant']
    
   
    