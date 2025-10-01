from django.db import models
from tenants.models import Tenant
from accounts.models import User
from django.conf import settings
from cryptography.fernet import Fernet

fernet = Fernet(settings.FERNET_KEY.encode())

class Contact(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="contacts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name="related_to")
    aceito = models.BooleanField(default=False)

    class Meta:
        unique_together = ("tenant", "user", "contact")

    def __str__(self):
        status = "Aceito" if self.aceito else "Pendente"
        return f"{self.user.username} ↔ {self.contact.username} ({status})"

class Chat(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="chats")
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_initiated")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_received")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tenant", "user1", "user2")

    def __str__(self):
        return f"Chat: {self.user1.username} & {self.user2.username} (Tenant: {self.tenant})"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    conteudo_encrypted = models.BinaryField()
    criado_em = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    @property
    def conteudo(self):
        return fernet.decrypt(self.conteudo_encrypted).decode()

    @conteudo.setter
    def conteudo(self, value):
        self.conteudo_encrypted = fernet.encrypt(value.encode())

    def __str__(self):
        try:
            preview = self.conteudo[:30]
        except Exception:
            preview = "<mensagem inválida>"
        return f"De {self.remetente.username} em {self.chat}: {preview}..."
