from django.db import models

from django.db import models

class Tenant(models.Model):
    tenant_id = models.AutoField(primary_key=True, unique=True)
    nome = models.CharField(max_length=255, null=False, blank=False)
    dominio = models.CharField(max_length=255, null=False, blank=False)
    logo_url = models.CharField(max_length=500, null=False, blank=False)
    paleta_de_cores = models.CharField(max_length=255, null=False, blank=False)
    criado_em = models.DateField( null=False, blank=False, auto_now_add=True)

    def __str__(self):
        return f"{self.tenant_id}, {self.nome}"
