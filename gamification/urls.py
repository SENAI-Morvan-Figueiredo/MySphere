from django.urls import path
from .views import TaskListView, UserTaskListView, PointsListView # LIST

urlpatterns = [
    path('task/', TaskListView.as_view(), name='task_list'), 
    path('usertask/', UserTaskListView.as_view(), name='user_task_list'), 
    path('points/', PointsListView.as_view(), name='point_list'), 
]