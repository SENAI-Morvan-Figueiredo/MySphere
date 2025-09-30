from django.urls import path
from . import views
from .views import novo, Users, UserLoginView, Home
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('usuarios/', Users.as_view(), name='users'),
    path('novo/', novo.as_view(), name='novo'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', Home.as_view(), name='home')
]