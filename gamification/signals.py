from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from accounts.models import User 
from gamification.models import Points, User_Task
from django.db.models import F

@receiver(post_save, sender=User)
def criar_registro_de_pontos(sender, instance, created, **kwargs):
    if created:
        tenant_do_usuario = instance.tenant 
        if tenant_do_usuario is not None:
            Points.objects.create(user=instance, pontos=0, nivel='Iniciante', tenant=tenant_do_usuario)
        else:
            print(tenant_do_usuario)   

# ADICIONAR OS PONTOS PARA O USUARIO QUANDO CONCLUIR

@receiver(pre_save, sender=User_Task)
def add_points_for_user(sender, instance, **kwargs):
    if not instance.pk:
        return

    previous = User_Task.objects.get(pk=instance.pk)

    if not previous.concluido and instance.concluido:
        task_pontos = instance.task.pontos

        points_obj, _ = Points.objects.get_or_create(
            user=instance.user,
            tenant=instance.user.tenant,
            defaults={'pontos': 0, 'nivel': 'Iniciante'},
        )

        points_obj.pontos = F('pontos') + task_pontos
        points_obj.save(update_fields=['pontos'])
