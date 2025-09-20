
from django.http import JsonResponse
# Create your views here.
def task_list( request) :
  data = {
    "tasks": [
      { "id": 1 , "title": "Buy Milk" , "completed": False }
    ]
  }
  return JsonResponse(data)