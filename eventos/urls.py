from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_eventos, name='listar_eventos'),
    path('criar_evento/', views.criar_evento, name='criar_evento'),
    path('<int:evento_id>/editar/', views.editar_evento, name='editar_evento'),
    path('<int:evento_id>/excluir/', views.excluir_evento, name='excluir_evento'),
    path('compacto/', views.listar_eventos, {'modo': 'compacto'}, name='listar_eventos_compacto'),
]
