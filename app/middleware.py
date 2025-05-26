from django.utils.deprecation import MiddlewareMixin

class CookieMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not request.COOKIES.get('theme_cookie'):
            response.set_cookie(
                'theme_cookie',
                'light',
                max_age=3600*24*30,  
                httponly=False,
                secure=request.is_secure(),
                samesite='Lax'
            )
        return response