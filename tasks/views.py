
from django.http import JsonResponse
# Create your views here.
def task_list( request) :
  data = {
    "tasks": [
      { "id": 1 , "title": "Buy Milk" , "completed": False },
      { "id": 2 , "title": "Buy an Orange" , "completed": False }
    ]
  }
  return JsonResponse(data)