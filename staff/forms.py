from django import forms
from accounts.models import User

class FormAddUsersStaff(forms.ModelForm):
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