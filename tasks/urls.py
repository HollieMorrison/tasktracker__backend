from django.urls import path
from . import views

urlpatterns = [
    path("tasks/" , views.task_list, name="task_list"),
    path("superuser/tasks/", views.superuser_tasks , name="superuser_tasks" )
]