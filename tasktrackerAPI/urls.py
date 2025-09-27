
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tasks/', include("tasks.urls")),
    path("user/", include("accounts.urls")),   # /user/login, /user/refresh, /user/me, /user/logout
]
