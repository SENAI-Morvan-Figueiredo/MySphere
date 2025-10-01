from django import forms
from .models import User

class UserForm(forms.ModelForm): # add user via superuser
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'tenant', 'data_nascimento', 'role', 'foto']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
    
class UserFormTenant(forms.ModelForm): # add user via staff
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'data_nascimento', 'role', 'foto']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user