from django.urls import path
from .views import novo, Users

urlpatterns = [
    path('usuarios/', Users.as_view(), name='users'),
    path('novo/', novo.as_view(), name='novo'),
]