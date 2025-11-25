from django.urls import path
from .views import GameHomeView, concluir_tarefa
from .views import TaskUpdateView, UserTaskUpdateView # EDIT
from .views import TaskDeleteView, UserTaskDeleteView # DELETE
from .views import ConquistaListView,  ConquistaUpdateView, ConquistaDeleteView # CONQUISTAS

urlpatterns = [
    
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),  
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),  
     
    path('usertask/<int:pk>/edit/', UserTaskUpdateView.as_view(), name='user_task_edit'),  
    path('usertask/<int:pk>/delete/', UserTaskDeleteView.as_view(), name='user_task_delete'),

    path('', GameHomeView.as_view(), name='game_home'), 
    path("usertask/<int:usertask_id>/concluir/", concluir_tarefa, name="concluir_tarefa"),

    path('conquista/', ConquistaListView.as_view(), name='conquista_list'),
    
    path('conquista/<int:pk>/edit/', ConquistaUpdateView.as_view(), name='conquista_edit'),
    path('conquista/<int:pk>/delete/', ConquistaDeleteView.as_view(), name='conquista_delete'),
]