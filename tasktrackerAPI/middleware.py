# tasktrackerAPI/middleware.py
from django.conf import settings
from django.http import HttpResponse

DEFAULT_ALLOWED = {
    "http://localhost:5173",
    "http://127.0.0.1:5173",
}
ALLOWED_ORIGINS = set(getattr(settings, "CORS_ALLOWED_ORIGINS", [])) or DEFAULT_ALLOWED


class AllowAllCORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin")

        # Preflight
        if request.method == "OPTIONS" and origin in ALLOWED_ORIGINS:
            resp = HttpResponse()
            resp["Access-Control-Allow-Origin"] = origin
            resp["Access-Control-Allow-Credentials"] = "true"
            resp["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            resp["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-CSRFToken"
            return resp

        response = self.get_response(request)
        if origin in ALLOWED_ORIGINS:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Expose-Headers"] = "Content-Type"
        return response
