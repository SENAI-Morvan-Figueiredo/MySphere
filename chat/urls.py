from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat_list, name="chat"),
    path("<int:chat_id>/", views.chat_detail, name="chat_detail"),
    path('criar_chat_ajax/', views.criar_chat_ajax, name='criar_chat_ajax'),
]
