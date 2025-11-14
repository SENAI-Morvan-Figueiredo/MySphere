from django.db import models
from colorfield.fields import ColorField

class Tenant(models.Model):
    tenant_id = models.AutoField(primary_key=True, unique=True)
    nome = models.CharField(max_length=255, null=False, blank=False)
    dominio = models.CharField(max_length=255, null=False, blank=False)
    logo_url = models.ImageField(upload_to="tenants/", null=True, blank=True)
    paleta_de_cores = ColorField(default='#FF0000')
    criado_em = models.DateField( null=False, blank=False, auto_now_add=True)

    def __str__(self):
        return f"{self.tenant_id}, {self.nome}"
