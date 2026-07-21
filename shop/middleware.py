class ApiCorsMiddleware:
    """Lets the Next.js frontend (any origin) read the /api/ endpoints."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/api/") or request.path.startswith("/media/"):
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        return response
