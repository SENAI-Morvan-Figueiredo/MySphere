from django.db import models
from tenants.models import Tenant
from accounts.models import User


from django.conf import settings
import base64
from cryptography.fernet import Fernet

fernet = Fernet(settings.FERNET_KEY.encode())

class Contact(models.Model):
    """
    Relação bilateral de contato entre dois usuários do mesmo tenant.
    Necessita convite/aceitação para ser efetivo.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="contacts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name="related_to")
    aceito = models.BooleanField(default=False)  # False = convite pendente

    class Meta:
        unique_together = ("tenant", "user", "contact")

    def save(self, *args, **kwargs):
        # Garante ordem fixa (sempre user1 < user2)
        if self.user1_id > self.user2_id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Aceito" if self.aceito else "Pendente"
        return f"{self.user.username} ↔ {self.contact.username} ({status})"


class Chat(models.Model):
    """
    Chat único entre dois usuários do mesmo tenant.
    Criado apenas após ambos serem contatos aceitos.
    """
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="chats")
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_initiated", null=True)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_received", null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tenant", "user1", "user2")

    def __str__(self):
        return f"Chat: {self.user1.username} & {self.user2.username} (Tenant: {self.tenant})"


class Message(models.Model):
    """
    Mensagens trocadas dentro de um chat.
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    conteudo_encrypted = models.BinaryField()

    @property
    def conteudo(self):
        return fernet.decrypt(self.conteudo_encrypted).decode()

    @conteudo.setter
    def conteudo(self, value):
        self.conteudo_encrypted = fernet.encrypt(value.encode())
    criado_em = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.remetente.username} em {self.chat}: {self.conteudo[:30]}..."