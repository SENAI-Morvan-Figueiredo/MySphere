from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import F
from accounts.models import User
from gamification.models import Points, User_Task, User_Conquista

# CRIA REGISTRO DE PONTOS PARA NOVO USUÁRIO
@receiver(post_save, sender=User)
def criar_registro_de_pontos(sender, instance, created, **kwargs):
    if created:
        tenant = instance.tenant

        if tenant is not None:
            Points.objects.create(
                user=instance,
                tenant=tenant,
                points_atual=0,
                points_total=0,
                nivel="Iniciante"
            )
        else:
            print("Usuário criado sem tenant:", instance.username)

@receiver(pre_save, sender=User_Task)
def add_points_and_conquista(sender, instance, **kwargs):

    if not instance.pk:
        return

    previous = User_Task.objects.get(pk=instance.pk)
    if not previous.concluido and instance.concluido:
        task = instance.task
        user = instance.user  
        points_obj, _ = Points.objects.get_or_create(
            user=user,
            tenant=user.tenant,
            defaults={
                'points_atual': 0,
                'points_total': 0,
                'nivel': 'Iniciante'
            }
        )

        points_obj.points_atual = F('points_atual') + task.pontos
        points_obj.save(update_fields=['points_atual'])

        if task.conquista:
            User_Conquista.objects.get_or_create(
                user=user,
                conquista=task.conquista
            )