from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),            # GET list, POST create
    path("<int:pk>/", views.task_detail, name="task_detail")# GET / PATCH / PUT single
]
