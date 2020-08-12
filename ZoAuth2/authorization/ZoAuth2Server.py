import os
from django.urls import reverse
from authlib.integrations.django_oauth2 import AuthorizationServer, ResourceProtector, BearerTokenValidator
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7523 import PrivateKeyJWT, private_key_jwt_sign, JWTBearerClientAssertion
from authlib.oauth2.rfc7662 import IntrospectionEndpoint
from .models import OAuth2Client, OAuth2Token
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZoAuth2.settings')


def now_timestamp():
    return int(time.time())

# TODO possibly move custom OAuth classes to a new lib/module
class ecdsaJWT(PrivateKeyJWT):
    """ecdsaJWT."""

    name = 'ecdsa_key_jwt'

    def sign(self, auth, token_endpoint):
        return private_key_jwt_sign(
            auth.client_secret,
            client_id=auth.client_id,
            token_endpoint=token_endpoint,
            alg='ES256',
            claims=self.claims,
        )

class JWTClientAuth(JWTBearerClientAssertion):
    """JWTClientAuth."""

    CLIENT_AUTH_METHOD = 'ecdsa_key_jwt'
    # TODO store and validate JTIs for real
    def validate_jti(self, claims, jti):
        key = 'jti:{}-{}'.format(claims['sub'], jti)
        print(key)
        return True

    def resolve_client_public_key(self, client, headers):
        return client.public_key


class ClientCredentialsGrant(grants.ClientCredentialsGrant):
    """ClientCredentialsGrant."""

    TOKEN_ENDPOINT_AUTH_METHODS = [
        'ecdsa_key_jwt'
    ]

class ZoAuth2IntrospectionEndpoint(IntrospectionEndpoint):
    """ZoAuthIntrospectionEndpoint."""


    def query_token(self, token, token_type_hint, client):
        """query_token.

        :param token:
        :param token_type_hint:
        :param client:
        """
        if token_type_hint == 'access_token':
            tok = OAuth2Token.objects.filter(access_token=token).first()
        elif token_type_hint == 'refresh_token':
            tok = OAuth2Token.objects.filter(refresh_token=token).first()
        else:
            tok = OAuth2Token.objects.filter(access_token=token).first()
            if not tok:
                tok = OAuth2Token.objects.filter(refresh_token=token).first()
        if tok:
            return tok
        #TODO  handle error more elegantly here
        return False
            #if has_introspect_permission(client):
            #    return tok

    @staticmethod
    def is_active(token):
        """is_active.

        :param token:
        """
        if now_timestamp() < token.get_expires_at() and not token.revoked:
            return True
        return False

    def introspect_token(self, token):
        """introspect_token.

        :param token:
        """
        #TODO validate the tokens activeness
        active = True
        return {
            'active': active,
            'client_id': token.client_id,
            'token_type': token.token_type,
            'username': token.user_id,
            'scope': token.get_scope(),
            'sub': 'placeholder', #TODO replace placeholder
            'aud': token.client_id,
            'iss': 'https://server.example.com/',
            'exp': token.get_expires_at(),
            'iat': token.issued_at,
        }

authorization = AuthorizationServer(
    client_model=OAuth2Client,
    token_model=OAuth2Token,
)
require_oauth = ResourceProtector()
authorization.register_grant(ClientCredentialsGrant)
authorization.register_client_auth_method(
    JWTClientAuth.CLIENT_AUTH_METHOD,
    JWTClientAuth('/authorization/token'))
authorization.register_endpoint(ZoAuth2IntrospectionEndpoint)
require_oauth.register_token_validator(BearerTokenValidator(OAuth2Token))
