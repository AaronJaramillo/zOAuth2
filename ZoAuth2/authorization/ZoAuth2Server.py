import os
from authlib.integrations.django_oauth2 import AuthorizationServer, ResourceProtector, BearerTokenValidator
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7523 import PrivateKeyJWT, private_key_jwt_sign, JWTBearerClientAssertion
from .models import OAuth2Client, OAuth2Token

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZoAuth2.settings')

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

authorization = AuthorizationServer(
    client_model=OAuth2Client,
    token_model=OAuth2Token,
)
require_oauth = ResourceProtector()
authorization.register_grant(ClientCredentialsGrant)
authorization.register_client_auth_method(
    JWTClientAuth.CLIENT_AUTH_METHOD,
    JWTClientAuth('http://127.0.0.1:8000/api/token'))
require_oauth.register_token_validator(BearerTokenValidator(OAuth2Token))
