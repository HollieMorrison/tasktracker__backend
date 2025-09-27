# DEV CORS middleware (no third-party packages)

ALLOWED_ORIGINS = {
    "http://localhost:5173",
    "http://127.0.0.1:5173",
}

class AllowAllCORSMiddleware:
    def _init_(self, get_response):
        self.get_response = get_response

    def _call_(self, request):
        origin = request.headers.get("Origin")

        # Handle preflight early
        if request.method == "OPTIONS" and origin in ALLOWED_ORIGINS:
            from django.http import HttpResponse
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