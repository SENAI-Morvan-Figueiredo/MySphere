from django import forms
from .models import Tenant

class TenantForm(forms.ModelForm):
    paleta_de_cores = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'type': 'color',  
                'class': 'form-control color-input',
            }
        )
    )

    class Meta:
        model = Tenant
        fields = ['nome', 'dominio', 'logo_url', 'paleta_de_cores']
