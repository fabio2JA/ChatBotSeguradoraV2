from django.contrib.auth import authenticate, login
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import cv2

class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            user = authenticate(request, username='admin', password='123')
            if user is not None:
                login(request, user)
        response = self.get_response(request)
        return response

class DisableCsrfCheck(MiddlewareMixin):

    def process_request(self, req):
        attr = '_dont_enforce_csrf_checks'
        if not getattr(req, attr, False):
            setattr(req, attr, True)
    