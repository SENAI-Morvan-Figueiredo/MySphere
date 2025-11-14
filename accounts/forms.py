from django import forms
from .models import User

class UserForm(forms.ModelForm): # add user via superuser
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'tenant', 'data_nascimento', 'role', 'foto']

    def save(self, commit=True):
        user = super().save(commit=False)
        nome = user.username.strip()
        letra_senha = nome[0].upper()
        data = user.data_nascimento
        data_senha = data.strftime("%Y%m%d")
        senha_gerada = f"{letra_senha}{data_senha}"
        user.set_password(senha_gerada)

        if commit:
            user.save()
        return user
    
class UserFormTenant(forms.ModelForm): # add user via staff
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'data_nascimento', 'role', 'foto', 'is_staff']

    def save(self, commit=True):
        user = super().save(commit=False)
        nome = user.username.strip()
        letra_senha = nome[0].upper()
        data = user.data_nascimento
        data_senha = data.strftime("%Y%m%d")
        senha_gerada = f"{letra_senha}{data_senha}"
        user.set_password(senha_gerada)

        if commit:
            user.save()
        return user