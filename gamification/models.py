from django.db import models
from tenants.models import Tenant
from accounts.models import User

class Task(models.Model):
    task_id = models.AutoField(primary_key=True, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="tasks")
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_creator")
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    pontos = models.PositiveIntegerField(default=0) 
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo}, {self.descricao}'

class User_Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_done")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="completed_by")    
    atribuido_por = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="tasks_assigned")
    concluido = models.BooleanField(default=False)
    concluido_em = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.concluido and not self.concluido_em:
            from django.utils import timezone   
            self.concluido_em = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} completou {self.task.titulo}"


class Points(models.Model):
    points_id = models.AutoField(primary_key=True, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="points")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="points_owner")
    pontos = models.PositiveIntegerField(default=0)
    nivel = models.CharField(max_length=50, null=False, blank=False) 
    ultima_atualizacao = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.user.username} - {self.pontos} pontos, ({self.nivel})"