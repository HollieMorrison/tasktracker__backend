from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def task_list(request):
    if request.method == "GET":
        qs = Task.objects.filter(Q(created_by=request.user) | Q(owners=request.user)).distinct()
        return Response(TaskSerializer(qs, many=True).data)

    # POST (create)
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        task = serializer.save(created_by=request.user)
        if task.owners.count() == 0:
            task.owners.add(request.user)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def task_detail(request, pk: int):
    """
    Retrieve, update, or delete a single task the user participates in.
    - GET     /api/tasks/<pk>/
    - PATCH   /api/tasks/<pk>/   (partial update)
    - PUT     /api/tasks/<pk>/   (full update)
    - DELETE  /api/tasks/<pk>/
    """
    try:
        task = Task.objects.filter(
            Q(created_by=request.user) | Q(owners=request.user)
        ).distinct().get(pk=pk)
    except Task.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(TaskSerializer(task).data)

    if request.method in ["PATCH", "PUT"]:
        partial = request.method == "PATCH"
        serializer = TaskSerializer(task, data=request.data, partial=partial)
        if serializer.is_valid():
            updated = serializer.save()
            if updated.owners.count() == 0:
                updated.owners.add(request.user)
            return Response(TaskSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
