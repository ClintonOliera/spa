from .models import Visit
from user_agents import parse

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Skip admin and static files
        if request.path.startswith("/admin") or request.path.startswith("/static"):
            return response

        ip = request.META.get("HTTP_X_FORWARDED_FOR") or request.META.get("REMOTE_ADDR")
        if ip:
            ip = ip.split(",")[0]

        ua_string = request.META.get("HTTP_USER_AGENT", "")
        ua = parse(ua_string)

        Visit.objects.create(
            ip_address=ip,
            path=request.path,
            browser=ua.browser.family,
            os=ua.os.family
        )

        return response
