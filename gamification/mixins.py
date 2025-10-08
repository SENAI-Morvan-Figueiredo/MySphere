# core/mixins.py
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, FieldDoesNotExist

logger = logging.getLogger(__name__)

class TenantAccessMixin(LoginRequiredMixin):
    tenant_field = "tenant"
    allow_superuser = True

    # utilitário: tenta obter o tenant do request.user
    def get_tenant(self):
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant is None and not self.request.user.is_superuser:
            raise PermissionDenied("Usuário sem tenant associado.")
        return tenant

    # utilitário: checa se o model tem determinado campo (mais robusto que iterar campos)
    def model_has_field(self, model, field_name):
        try:
            model._meta.get_field(field_name)
            return True
        except FieldDoesNotExist:
            return False

    # resolve o tenant de uma instância (obj) de forma genérica
    def resolve_tenant_from_instance(self, obj):
        Model = obj.__class__
        if self.model_has_field(Model, 'tenant'):
            return getattr(obj, 'tenant', None)
        if self.model_has_field(Model, 'task'):
            task = getattr(obj, 'task', None)
            return getattr(task, 'tenant', None) if task else None
        if self.model_has_field(Model, 'user'):
            user = getattr(obj, 'user', None)
            return getattr(user, 'tenant', None) if user else None
        return None

    # aplica tenant/criador apenas em criação e apenas se os campos existirem
    def set_tenant_and_creator(self, form):
        # somente em criação (instance sem PK)
        if getattr(form.instance, 'pk', None) is not None:
            return form

        tenant = self.get_tenant()

        # define tenant se o modelo tiver o campo tenant
        if self.model_has_field(form.instance.__class__, 'tenant'):
            form.instance.tenant = tenant

        # define o campo de quem criou (criado_por) se existir
        if self.model_has_field(form.instance.__class__, 'criado_por'):
            form.instance.criado_por = self.request.user
        # se o modelo usa "atribuido_por" (ex: User_Task), define isso em vez de criado_por
        elif self.model_has_field(form.instance.__class__, 'atribuido_por'):
            # só define se ainda não veio do formulário
            if not getattr(form.instance, 'atribuido_por', None):
                form.instance.atribuido_por = self.request.user

        return form

    # filtra o queryset de acordo com o tenant do usuário
    def get_queryset(self):
        queryset = super().get_queryset()

        # superuser com permissão pode ver tudo
        if self.request.user.is_superuser and self.allow_superuser:
            return queryset

        tenant = getattr(self.request.user, "tenant", None)
        if not tenant:
            return queryset.none()

        Model = self.model
        if self.model_has_field(Model, 'tenant'):
            return queryset.filter(tenant=tenant)
        if self.model_has_field(Model, 'task'):
            return queryset.filter(task__tenant=tenant)
        if self.model_has_field(Model, 'user'):
            return queryset.filter(user__tenant=tenant)

        # fallback seguro
        return queryset.none()

    # proteções extras ao obter um objeto (update/delete/detail)
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        # se superuser liberado, pula checagem
        if self.request.user.is_superuser and self.allow_superuser:
            return obj

        obj_tenant = self.resolve_tenant_from_instance(obj)
        if obj_tenant != self.get_tenant():
            raise PermissionDenied("Acesso negado a objeto de outro tenant.")
        return obj

    # executado quando o form é válido (Create/Update) — só chamamos o set_tenant_and_creator
    def form_valid(self, form):
        # só aplicar em criação; set_tenant_and_creator já faz a checagem
        form = self.set_tenant_and_creator(form)
        return super().form_valid(form)

    # filtrar querysets de campos do form (ModelChoiceFields)
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # se superuser, não limite nada
        if self.request.user.is_superuser and self.allow_superuser:
            return form

        tenant = getattr(self.request.user, "tenant", None)
        for field_name, field in form.fields.items():
            if hasattr(field, "queryset") and field.queryset is not None:
                try:
                    model = field.queryset.model
                    if not tenant:
                        field.queryset = field.queryset.none()
                        continue

                    if self.model_has_field(model, 'tenant'):
                        field.queryset = field.queryset.filter(tenant=tenant)
                    elif self.model_has_field(model, 'task'):
                        field.queryset = field.queryset.filter(task__tenant=tenant)
                    elif self.model_has_field(model, 'user'):
                        field.queryset = field.queryset.filter(user__tenant=tenant)
                except Exception as e:
                    logger.debug("Erro filtrando queryset do campo %s: %s", field_name, e)
                    continue
        return form
