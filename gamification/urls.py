from django.urls import path
from .views import TaskListView, UserTaskListView, PointsListView # LIST 
from .views import GameHomeView, concluir_tarefa
from .views import TaskCreateView, UserTaskCreateView # CREATE
from .views import TaskUpdateView, UserTaskUpdateView # EDIT
from .views import TaskDeleteView, UserTaskDeleteView # DELETE

urlpatterns = [
    path('task/lista/', TaskListView.as_view(), name='task_list'),  # STAFF
    path('task/novo/', TaskCreateView.as_view(), name='task_create'),  # STAFF
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),  # STAFF
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),  # STAFF
    path('usertask/', UserTaskListView.as_view(), name='user_task_list'),  # STAFF
    path('usertask/novo/', UserTaskCreateView.as_view(), name='user_task_create'),  # STAFF
    path('usertask/<int:pk>/edit/', UserTaskUpdateView.as_view(), name='user_task_edit'),  # STAFF
    path('usertask/<int:pk>/delete/', UserTaskDeleteView.as_view(), name='user_task_delete'),  # STAFF
    path('points/lista/', PointsListView.as_view(), name='point_list'), # STAFF
    path('', GameHomeView.as_view(), name='game_home'), # USER
    path('usertask/<int:task_id>/concluir/', concluir_tarefa, name='concluir_tarefa'), # USER
]