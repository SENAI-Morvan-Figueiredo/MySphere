from django.db import models
from tenants.models import Tenant

class User(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="tenant")
    nome = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    senha = models.CharField(max_length=255, null=False, blank=False)
    role = models.CharField(max_length=100, null=False, blank=False)
    foto = models.ImageField(upload_to="accounts/", null=True, blank=True)
    status = models.BooleanField(default=True, null=False)
    criado_em = models.DateField(auto_now_add=True, null=False, blank=False)
    data_nascimento = models.DateField(null=False, blank=False)

    def __str__(self):
        return f"{self.user_id}, {self.nome}"