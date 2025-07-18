from jose import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header
import requests

class Auth0User:
    def __init__(self, payload):
        self.payload = payload
        self.auth0_id = payload.get('sub')
        self.email = payload.get('email', '')
        self.permissions = payload.get('permissions', [])
        self.roles = payload.get('https://my-app.example.com/roles', [])
        
    def __str__(self):
        return f"Auth0User({self.auth0_id})"
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

class Auth0Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()
        
        if not auth_header or auth_header[0].lower() != b'bearer':
            return None
        
        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Authorization header inválido: No se proveyó el token.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Authorization header inválido: El token no debe contener espacios.')
        
        token = auth_header[1]
        
        try:
            jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
            jwks = requests.get(jwks_url).json()
            
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
            
            if not rsa_key:
                raise exceptions.AuthenticationFailed('No se encontró la clave pública apropiada.')
            
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=settings.AUTH0_API_AUDIENCE,
                issuer=f"https://{settings.AUTH0_DOMAIN}/"
            )
            
            
            user = Auth0User(payload)
            
            return (user, payload)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('El token ha expirado.')
        except jwt.JWTClaimsError as e:
            raise exceptions.AuthenticationFailed('Claims inválidos. Revisa el audience y el issuer.')
        except Exception as e:
            raise exceptions.AuthenticationFailed('Error al decodificar el token.')