from django import forms
from .models import Tenant

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['nome', 'dominio', 'logo_url', 'paleta_de_cores']