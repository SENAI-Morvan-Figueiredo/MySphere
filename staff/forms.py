from django import forms
from accounts.models import User

class FormAddUsersStaff(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'data_nascimento', 'role', 'foto']
        help_texts = {'username': ''}

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