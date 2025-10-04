
from django.core.management.base import BaseCommand
from tenants.models import Tenant
from accounts.models import User
from datetime import date

class Command(BaseCommand):
    help = 'Cria dois tenants e um usuário para cada um para testes'

    def handle(self, *args, **options):
        # Criar Tenant 1
        tenant1, created1 = Tenant.objects.get_or_create(
            nome='Empresa Alpha',
            defaults={
                'dominio': 'alpha.example.com',
                'logo_url': 'https://via.placeholder.com/150/0000FF/FFFFFF?text=Alpha',
                'paleta_de_cores': '#0000FF,#FFFFFF,#CCCCCC'
            }
        )
        if created1:
            self.stdout.write(self.style.SUCCESS(f'Tenant "{tenant1.nome}" criado com ID {tenant1.tenant_id}'))
        else:
            self.stdout.write(self.style.WARNING(f'Tenant "{tenant1.nome}" já existe com ID {tenant1.tenant_id}'))

        # Criar Tenant 2
        tenant2, created2 = Tenant.objects.get_or_create(
            nome='Empresa Beta',
            defaults={
                'dominio': 'beta.example.com',
                'logo_url': 'https://via.placeholder.com/150/FF0000/FFFFFF?text=Beta',
                'paleta_de_cores': '#FF0000,#FFFFFF,#EEEEEE'
            }
        )
        if created2:
            self.stdout.write(self.style.SUCCESS(f'Tenant "{tenant2.nome}" criado com ID {tenant2.tenant_id}'))
        else:
            self.stdout.write(self.style.WARNING(f'Tenant "{tenant2.nome}" já existe com ID {tenant2.tenant_id}'))

        # Criar usuário para Tenant 1
        user1_username = 'usuario_alpha'
        user1_email = 'usuario@alpha.com'
        
        if not User.objects.filter(username=user1_username).exists():
            user1 = User.objects.create_user(
                username=user1_username,
                email=user1_email,
                password='senha123',
                tenant=tenant1,
                role='Funcionário',
                data_nascimento=date(1990, 1, 15),
                first_name='João',
                last_name='Alpha'
            )
            self.stdout.write(self.style.SUCCESS(f'Usuário "{user1.username}" criado para {tenant1.nome}'))
            self.stdout.write(f'  Email: {user1_email}')
            self.stdout.write(f'  Senha: senha123')
        else:
            self.stdout.write(self.style.WARNING(f'Usuário "{user1_username}" já existe'))

        # Criar usuário para Tenant 2
        user2_username = 'usuario_beta'
        user2_email = 'usuario@beta.com'
        
        if not User.objects.filter(username=user2_username).exists():
            user2 = User.objects.create_user(
                username=user2_username,
                email=user2_email,
                password='senha123',
                tenant=tenant2,
                role='Gerente',
                data_nascimento=date(1985, 5, 20),
                first_name='Maria',
                last_name='Beta'
            )
            self.stdout.write(self.style.SUCCESS(f'Usuário "{user2.username}" criado para {tenant2.nome}'))
            self.stdout.write(f'  Email: {user2_email}')
            self.stdout.write(f'  Senha: senha123')
        else:
            self.stdout.write(self.style.WARNING(f'Usuário "{user2_username}" já existe'))

        self.stdout.write(self.style.SUCCESS('\n=== Resumo ==='))
        self.stdout.write(f'Tenant 1: {tenant1.nome} (ID: {tenant1.tenant_id})')
        self.stdout.write(f'  Usuário: usuario_alpha / senha123')
        self.stdout.write(f'\nTenant 2: {tenant2.nome} (ID: {tenant2.tenant_id})')
        self.stdout.write(f'  Usuário: usuario_beta / senha123')
