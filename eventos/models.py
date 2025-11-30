from django.db import models
from django.conf import settings
from accounts.models import Tenant

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="tenant_evento")
    foto = models.ImageField(upload_to="eventos/", null=True, blank=True)

def __str__(self):
    return self.titulo
