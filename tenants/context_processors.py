from .models import Tenant

def tenant_context(request):
    user = request.user

    if not user.is_authenticated or user.is_superuser:
        return {"tenant": None}
    if hasattr(user, "tenant"):
        try:
            return {
                "tenant": Tenant.objects.get(pk=user.tenant.pk)
            }
        except Tenant.DoesNotExist:
            return {"tenant": None}
    return {"tenant": None}
