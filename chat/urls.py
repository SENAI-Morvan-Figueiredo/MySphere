from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat_list, name="chat"),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('visualizar/<int:msg_id>/<str:tipo>/', views.visualizar_arquivo, name='visualizar_arquivo'),
    path('criar_chat_ajax/', views.criar_chat_ajax, name='criar_chat_ajax'),
    path('atualizar_chats/', views.atualizar_chats, name='atualizar_chats'),
    path("chat/<int:chat_id>/atualizar/", views.atualizar_mensagens, name="atualizar_mensagens"),

]
