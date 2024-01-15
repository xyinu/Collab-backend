import jwt
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError
User = get_user_model()
from dotenv import load_dotenv
import os
from jwt import PyJWKClient

load_dotenv()
MICROSOFT_CLIENT_ID = os.getenv('MICROSOFT_CLIENT_ID')

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')

        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)  # clean the token
        url = "https://login.microsoftonline.com/common/discovery/v2.0/keys"
        optional_custom_headers = {"User-agent": "custom-user-agent"}
        jwks_client = PyJWKClient(url, headers=optional_custom_headers)
        signing_key = jwks_client.get_signing_key_from_jwt(jwt_token)
        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token,
                                 signing_key.key,
                                 algorithms=["RS256"],
                                 audience=MICROSOFT_CLIENT_ID,
                                 options={"verify_exp": False},
                                 )
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        # Get the user from the database
        email = payload.get('preferred_username').lower()
        print(payload)#test for prof email
        if email is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if(not user.name):
           name = payload.get('name').lower().replace('#','')
           user.name=name
           user.save()

        # Return the user and token payload
        return user, payload

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token