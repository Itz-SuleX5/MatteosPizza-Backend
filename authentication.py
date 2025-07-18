from rest_framework import authentication, exceptions
from jose import jwt
import requests
from django.conf import settings

class Auth0JSONWebTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        parts = auth_header.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            raise exceptions.AuthenticationFailed('Authorization header must be Bearer token')

        token = parts[1]

        jwks_url = f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json'
        jwks = requests.get(jwks_url).json()

        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if not rsa_key:
            raise exceptions.AuthenticationFailed('RSA key not found')

        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=settings.ALGORITHMS,
                audience=settings.API_IDENTIFIER,
                issuer=f'https://{settings.AUTH0_DOMAIN}/'
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expirado')
        except jwt.JWTClaimsError:
            raise exceptions.AuthenticationFailed('Claims inválidos')
        except Exception:
            raise exceptions.AuthenticationFailed('Token inválido')

        # Aquí puedes buscar/crear usuario Django si quieres
        # Por ahora retornamos None y el payload
        return (None, payload)
