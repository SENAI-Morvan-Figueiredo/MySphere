from .models import Tenant

def tenant_context(request):
    if request.user.is_authenticated and hasattr(request.user, "tenant"):
        try:
            return {
                "tenant": Tenant.objects.get(pk=request.user.tenant.pk)
            }
        except Tenant.DoesNotExist:
            return {"tenant": None}
    return {"tenant": None}
