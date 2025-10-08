from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User 
from gamification.models import Points

@receiver(post_save, sender=User)
def criar_registro_de_pontos(sender, instance, created, **kwargs):
    if created:
        tenant_do_usuario = instance.tenant 
        if tenant_do_usuario is not None:
            Points.objects.create(user=instance, pontos=0, nivel='Iniciante', tenant=tenant_do_usuario)
        else:
            print(tenant_do_usuario)    