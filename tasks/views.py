from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Task

def superuser_tasks(request):
    """
    Returns all tasks created by the superuser(s) in JSON format.
    """
    User = get_user_model()
    superusers = User.objects.filter(is_superuser=True)

    tasks = Task.objects.filter(created_by__in=superusers).values(
        "id",
        "title",
        "description",
        "priority",
        "state",
        "due_date",
        "is_overdue",
        "created_at",
        "updated_at",
        "category__name",
        "created_by__username",
    )

    return JsonResponse(list(tasks), safe=False)

# Create your views here.
def task_list( request) :
  data = {
    "tasks": [
      { "id": 1 , "title": "Buy Milk" , "completed": False },
      { "id": 2 , "title": "Buy an Orange" , "completed": False }
    ]
  }
  return JsonResponse(data)