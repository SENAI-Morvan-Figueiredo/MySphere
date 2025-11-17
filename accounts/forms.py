from django import forms
from .models import User
    
class UserFormTenant(forms.ModelForm): # add user via staff

    class Meta:
        model = User
        fields = ['username', 'email', 'data_nascimento', 'role', 'foto', 'is_staff']

    def save(self, commit=True):
        user = super().save(commit=False)
        nome = user.username.strip()
        letra_senha = nome[0].upper()
        data = user.data_nascimento
        data_senha = data.strftime("%d%m%Y")
        senha_gerada = f"{letra_senha}{data_senha}"
        print(f'Senha aqui: {senha_gerada}')
        user.set_password(senha_gerada)

        if commit:
            user.save()
        return user
    
class UserFormStaff(forms.ModelForm): 

    class Meta:
        model = User
        fields = ['username', 'email', 'data_nascimento', 'role', 'foto']

    def save(self, commit=True):
        user = super().save(commit=False)
        nome = user.username.strip()
        letra_senha = nome[0].upper()
        data = user.data_nascimento
        data_senha = data.strftime("%d%m%Y")
        senha_gerada = f"{letra_senha}{data_senha}"
        print(f'Senha aqui: {senha_gerada}')
        user.set_password(senha_gerada)

        if commit:
            user.save()
        return user
    
class UserEditFormStaff(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'data_nascimento', 'role', 'foto']
