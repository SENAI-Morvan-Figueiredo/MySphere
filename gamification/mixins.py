# mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class TenantAccessMixin(LoginRequiredMixin):
    
    tenant_field = "tenant"
    allow_superuser = True

    def get_tenant(self):
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant is None and not self.request.user.is_superuser:
            raise PermissionDenied("Usuário sem tenant associado.")
        return tenant

    def set_tenant_and_creator(self, form):
        form.instance.criado_por = self.request.user
        tenant_id = self.kwargs.get("pk")
        form.instance.tenant_id = tenant_id or self.request.user.tenant_id
        return form

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = getattr(self.request.user, "tenant", None)

        if not tenant and not self.request.user.is_superuser:
            return queryset.none()

        model_fields = [f.name for f in self.model._meta.get_fields()]

        if 'tenant' in model_fields:
            return queryset.filter(tenant=tenant)
        elif 'task' in model_fields:
            return queryset.filter(task__tenant=tenant)
        elif 'user' in model_fields:
            return queryset.filter(user__tenant=tenant)
        else:
            return queryset.none()

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)

        if not (self.request.user.is_superuser and self.allow_superuser):
            obj_tenant = getattr(obj, self.tenant_field, None)
            if obj_tenant != self.get_tenant():
                raise PermissionDenied("Acesso negado a objeto de outro tenant.")
        return obj

    def form_valid(self, form):
        form = self.set_tenant_and_creator(form)
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tenant = getattr(self.request.user, "tenant", None)

        for field_name, field in form.fields.items():
            if hasattr(field, "queryset"):
                try:
                    model = field.queryset.model
                    model_fields = [f.name for f in model._meta.get_fields()]

                    if 'tenant' in model_fields:
                        field.queryset = field.queryset.filter(tenant=tenant)

                    elif 'task' in model_fields:
                        field.queryset = field.queryset.filter(task__tenant=tenant)

                    elif 'user' in model_fields:
                        field.queryset = field.queryset.filter(user__tenant=tenant)

                except Exception:
                    continue
        return form
