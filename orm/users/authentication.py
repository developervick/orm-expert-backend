from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Read from cookie instead of Authorization header
        access_token = request.COOKIES.get('accesstoken') or request.COOKIES.get('accessToken')
        
        if not access_token:
            return None  # fall through to next authenticator
        
        # rest is same as normal JWT auth
        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token 