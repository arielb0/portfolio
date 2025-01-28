from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.request import Request
from django.contrib.auth.models import User

class CookieJWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request: Request):
        token = request.COOKIES.get('access_token')
        
        if not token:
            return None
        
        try:
            validated_token = AccessToken(token)
        except Exception as e:
            raise AuthenticationFailed('Invalid or expired token!')
        
        user_id = validated_token.get('user_id')
        try:            
            user = User.objects.get(id = user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found!')
                
        return (user, validated_token)
    