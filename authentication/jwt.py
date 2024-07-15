from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
import jwt
from .models import User

class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()
        
        if not auth_header or auth_header[0].lower() != b'bearer':
            return None
        
        if len(auth_header) != 2:
            raise exceptions.AuthenticationFailed("Token is not valid")
        
        token = auth_header[1]
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            username = payload["username"]
            user = User.objects.get(username=username)
            return (user, token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("No such user")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token is expired, login again")
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Token is invalid")
        
        return None
