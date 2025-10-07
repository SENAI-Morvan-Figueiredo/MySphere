from django.urls import path
from .views import TaskListView, UserTaskListView, PointsListView, PointsUserView # LIST
from .views import TaskCreateView, UserTaskCreateView # CREATE
from .views import TaskUpdateView, UserTaskUpdateView # EDIT
from .views import TaskDeleteView, UserTaskDeleteView # DELETE

urlpatterns = [
    path('task/', TaskListView.as_view(), name='task_list'), 
    path('task/novo/', TaskCreateView.as_view(), name='task_create'), 
    path('task/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'), 
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'), 
    path('usertask/', UserTaskListView.as_view(), name='user_task_list'), 
    path('usertask/novo/', UserTaskCreateView.as_view(), name='user_task_create'), 
    path('usertask/<int:pk>/edit/', UserTaskUpdateView.as_view(), name='user_task_edit'), 
    path('usertask/<int:pk>/delete/', UserTaskDeleteView.as_view(), name='user_task_delete'), 
    path('points/lista/', PointsListView.as_view(), name='point_list'), # STAFF
    path('points/', PointsUserView.as_view(), name='points_user'), # USER
]