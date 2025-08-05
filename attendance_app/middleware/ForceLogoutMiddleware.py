from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings

class ForceLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Keep only login/admin/static/media pages accessible
            safe_paths = ['/admin/login', '/login', '/static', '/media']
            if not any(request.path.startswith(p) for p in safe_paths):
                logout(request)
                return redirect(settings.LOGIN_URL)

        return self.get_response(request)
