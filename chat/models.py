from django.db import models
from tenants.models import Tenant
from accounts.models import User

class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="chats")
    tipo = models.CharField(max_length=20)
    criado_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.chat_id} ({self.tipo}) - Tenant {self.tenant_id}"

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_received")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    conteudo = models.TextField()
    criado_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Tenant: {self.tenant}, Chat: {self.chat}, De: {self.user}, Para: {self.destinatario}, Mensagem: {self.conteudo[:30]}..."
