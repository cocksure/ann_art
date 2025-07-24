from django.utils import translation

class SetLanguageCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        lang = translation.get_language()
        response.set_cookie('django_language', lang)
        return response