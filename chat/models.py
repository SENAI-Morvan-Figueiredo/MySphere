from django.db import models
from tenants.models import Tenant
from accounts.models import User
from django.conf import settings
from cryptography.fernet import Fernet
import io
import os
from django.core.files.base import ContentFile

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
    imagem = models.ImageField(upload_to="posts/", null=True, blank=True)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    arquivo = models.FileField(upload_to="files/", null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    lido = models.BooleanField(default=False)

    @property
    def conteudo(self):
        """
        Retorna o texto descriptografado.
        Se der erro, retorna None (e não a string "<mensagem corrompida>").
        """
        try:
            fernet = Fernet(settings.FERNET_KEY.encode())
            return fernet.decrypt(bytes(self.conteudo_encrypted)).decode()
        except Exception:
            return None

    @conteudo.setter
    def conteudo(self, value):
        fernet = Fernet(settings.FERNET_KEY.encode())
        self.conteudo_encrypted = fernet.encrypt(value.encode())

    @property
    def conteudo_corrompido(self):
        """Retorna True se falhar a descriptografia."""
        try:
            fernet = Fernet(settings.FERNET_KEY.encode())
            fernet.decrypt(bytes(self.conteudo_encrypted))
            return False
        except Exception:
            return True


    # ----------- NOME ORIGINAL DOS ARQUIVOS (sem .enc) -----------

    def _original_name_from_field(self, field):
        if not field:
            return None
        try:
            name = os.path.basename(field.name)
            if name.endswith('.enc'):
                name = name[:-4]
            return name
        except Exception:
            return None

    @property
    def imagem_nome(self):
        return self._original_name_from_field(self.imagem)

    @property
    def video_nome(self):
        return self._original_name_from_field(self.video)

    @property
    def arquivo_nome(self):
        return self._original_name_from_field(self.arquivo)

    @property
    def arquivo_tamanho(self):
        """Tamanho aproximado do arquivo."""
        f = self.arquivo
        if not f:
            return None
        try:
            kb = max(1, f.size // 1024)
            return f"{kb} KB"
        except Exception:
            return None
     # === Criptografia de arquivos ===
    def save(self, *args, **kwargs):

        if self.imagem and not self.imagem.name.endswith(".enc"):
            # 🟢 Adicionar para garantir que a leitura comece do início
            self.imagem.file.seek(0) 
            original_data = self.imagem.read()
            encrypted_data = fernet.encrypt(original_data)
            self.imagem.save(self.imagem.name + ".enc", ContentFile(encrypted_data), save=False)

        if self.video and not self.video.name.endswith(".enc"):
            # 🟢 CORREÇÃO: Adicionar seek(0) aqui!
            self.video.file.seek(0) 
            original_data = self.video.read()
            encrypted_data = fernet.encrypt(original_data)
            self.video.save(self.video.name + ".enc", ContentFile(encrypted_data), save=False)

        # Criptografa arquivo
        if self.arquivo and not self.arquivo.name.endswith(".enc"):
            # 🟢 Adicionar para garantir que a leitura comece do início
            self.arquivo.file.seek(0) 
            original_data = self.arquivo.read()
            encrypted_data = fernet.encrypt(original_data)
            self.arquivo.save(self.arquivo.name + ".enc", ContentFile(encrypted_data), save=False)

        super().save(*args, **kwargs)

    # === Descriptografia ao acessar o arquivo ===
    def get_decrypted_file(self, file_field):
        if not file_field:
            return None
        encrypted_data = file_field.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        return io.BytesIO(decrypted_data)
