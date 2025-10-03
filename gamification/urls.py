from django.urls import path
from .views import TaskListView, UserTaskListView, PointsListView # LIST
from .views import TaskCreateView, UserTaskCreateView # CREATE

urlpatterns = [
    path('task/', TaskListView.as_view(), name='task_list'), 
    path('task/novo/', TaskCreateView.as_view(), name='task_create'), 
    path('usertask/', UserTaskListView.as_view(), name='user_task_list'), 
    path('usertask/novo/', UserTaskCreateView.as_view(), name='user_task_create'), 
    path('points/', PointsListView.as_view(), name='point_list'), 
]