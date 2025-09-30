# accounts/management/commands/createsuperuser.py
from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from tenants.models import Tenant
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--tenant",
            type=int,
            help="ID do Tenant ao qual o superuser pertencerá",
        )

    def handle(self, *args, **options):
        tenant_id = options.get("tenant")

        if tenant_id:
            try:
                options["tenant"] = Tenant.objects.get(pk=tenant_id)
            except ObjectDoesNotExist:
                self.stderr.write(self.style.ERROR(f"Tenant com ID {tenant_id} não existe"))
                return
        else:
            default_tenant = Tenant.objects.first()
            if not default_tenant:
                self.stderr.write(self.style.ERROR("Nenhum Tenant existe no banco. Crie um primeiro."))
                return
            options["tenant"] = default_tenant

        super().handle(*args, **options)

