from django.contrib.auth import authenticate, login

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
    