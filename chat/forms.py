# chat/forms.py
from django import forms
from .models import Message
from django.conf import settings
from cryptography.fernet import Fernet

fernet = Fernet(settings.FERNET_KEY.encode())

class MessageForm(forms.ModelForm):
    conteudo = forms.CharField(
        label="Mensagem",
        widget=forms.TextInput(attrs={"placeholder": "Digite sua mensagem..."})
    )

    class Meta:
        model = Message
        fields = []  # não usamos campos diretos do modelo, apenas o 'conteudo' virtual

    def save(self, commit=True, remetente=None, chat=None):
        msg_text = self.cleaned_data['conteudo']
        instance = Message(
            remetente=remetente,
            chat=chat,
            conteudo_encrypted=fernet.encrypt(msg_text.encode())
        )
        if commit:
            instance.save()
        return instance
