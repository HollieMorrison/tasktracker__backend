# views.py
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def task_list(request):
    if request.method == "GET":
        qs = Task.objects.filter(Q(created_by=request.user) | Q(owners=request.user)).distinct()
        return Response(TaskSerializer(qs, many=True).data)

    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(created_by=request.user)
            if task.owners.count() == 0:
                task.owners.add(request.user)
            return Response(TaskSerializer(task).data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def superuser_tasks(request):
    qs = Task.objects.all()
    return Response(TaskSerializer(qs, many=True).data)
