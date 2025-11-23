from django.core.management.base import BaseCommand
from django.db.models import F
from django.utils import timezone
from gamification.models import Points, Conquista, User_Conquista
from tenants.models import Tenant

class Command(BaseCommand):
    help = "Processa o ranking mensal, gera conquistas e zera pontos atuais."

    def handle(self, *args, **kwargs):
        agora = timezone.now()
        mes = agora.strftime("%m")
        ano = agora.strftime("%Y")
        nome_conquista = f"TOP 5 - Ranking Mensal {mes}/{ano}"

        for tenant in Tenant.objects.all():

            self.stdout.write(f"Tenant: {tenant.nome}")

            # Ranking baseado nos pontos atuais
            ranking = Points.objects.filter(tenant=tenant).order_by("-points_atual")[:5]

            if not ranking:
                self.stdout.write(" Nenhum usuário com pontos.")
                continue

            # Cria conquista do mês
            conquista, _ = Conquista.objects.get_or_create(
                tenant=tenant,
                nome=nome_conquista,
                defaults={
                    "descricao": f"Conquista entregue aos Top 5 do mês {mes}/{ano}",
                    "ranking_mensal": True
                }
            )

            # Entregar conquistas aos top 5
            for pontos_obj in ranking:
                User_Conquista.objects.get_or_create(
                    user=pontos_obj.user,
                    conquista=conquista
                )
                self.stdout.write(f"{pontos_obj.user.username} recebeu conquista TOP 5")

            Points.objects.filter(tenant=tenant).update(
                points_total=F('points_total') + F('points_atual'),
                points_atual=0
            )

            self.stdout.write("Pontos transferidos e zerados.\n")

