from django.db import models
from django.db.models import F
from tenants.models import Tenant
from accounts.models import User
from django.core.exceptions import ValidationError

class Conquista(models.Model):
    conquista_id = models.AutoField(primary_key=True, unique=True)
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to="conquistas/", blank=True, null=True)
    ranking_mensal = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="conquistas", null=True)

    def __str__(self):
        return self.nome


class Task(models.Model):
    task_id = models.AutoField(primary_key=True, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="tasks")
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_creator")
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)
    pontos = models.PositiveIntegerField(default=0)
    conquista = models.ForeignKey(Conquista, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks_with_badge")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo}, {self.descricao}'


class User_Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks_done")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="completed_by")
    atribuido_por = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="tasks_assigned")
    concluido = models.BooleanField(default=False)
    concluido_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'task')

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
    points_atual = models.PositiveIntegerField(default=0)
    points_total = models.PositiveIntegerField(default=0)
    nivel = models.CharField(max_length=50, null=False, blank=False, default='Iniciante')
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.points_total} pontos, ({self.nivel})"

    def atualizar_nivel(self):
        if self.points_total >= 1000:
            novo = 'Avançado'
        elif self.points_total >= 500:
            novo = 'Intermediário'
        else:
            novo = 'Iniciante'

        if self.nivel != novo:
            self.nivel = novo
            self.save(update_fields=['nivel'])

    def add_points(self, pontos):
        self.points_atual = F('points_atual') + pontos
        self.save()
        self.refresh_from_db()
        self.atualizar_nivel()


class User_Conquista(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conquists_received")
    conquista = models.ForeignKey(Conquista, on_delete=models.CASCADE, related_name="users_received")
    recebido_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "conquista")

    def __str__(self):
        return f"{self.user.username} ganhou a conquista {self.conquista.nome}"
