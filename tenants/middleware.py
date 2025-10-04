from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.urls import resolve
from .models import Tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.tenant = request.user.tenant
        else:
            request.tenant = None
        
        response = self.get_response(request)
        return response
