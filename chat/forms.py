# chat/forms.py
from django import forms
from .models import Message, Chat
from accounts.models import User
from django.conf import settings
from cryptography.fernet import Fernet

fernet = Fernet(settings.FERNET_KEY.encode())

from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    conteudo = forms.CharField(
        label="Mensagem",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Digite sua mensagem..."})
    )

    class Meta:
        model = Message
        fields = ["conteudo", "imagem", "video", "arquivo"]

    def save(self, commit=True, remetente=None, chat=None):
        instance = super().save(commit=False)
        if remetente:
            instance.remetente = remetente
        if chat:
            instance.chat = chat

        # Criptografa o texto
        if self.cleaned_data.get("conteudo"):
            instance.conteudo = self.cleaned_data["conteudo"]

        if commit:
            instance.save()
        return instance

class ChatForm(forms.Form):
    email = forms.EmailField(
        label="E-mail do usuário",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Digite o e-mail"})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.tenant = kwargs.pop("tenant", None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user2 = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("Usuário não encontrado.")

        if user2.tenant != self.tenant:
            raise forms.ValidationError("Usuário não pertence ao mesmo tenant.")

        if Chat.objects.filter(
            tenant=self.tenant,
            user1=self.user,
            user2=user2
        ).exists() or Chat.objects.filter(
            tenant=self.tenant,
            user1=user2,
            user2=self.user
        ).exists():
            raise forms.ValidationError("Um chat entre vocês já existe.")

        return email

    def save(self):
        user2 = User.objects.get(email=self.cleaned_data["email"])
        chat = Chat.objects.create(tenant=self.tenant, user1=self.user, user2=user2)
        return chat
