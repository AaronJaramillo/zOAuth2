import os
from authlib.integrations.django_oauth2 import (
    AuthorizationServer,
    ResourceProtector,
    BearerTokenValidator)
from .models import OAuth2Client, OAuth2Token
from .ZoAuth2 import (
    ClientCredentialsGrant,
    JWTClientAuth,
    ZoAuth2IntrospectionEndpoint
)
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZoAuth2.settings')


authorization = AuthorizationServer(
    client_model=OAuth2Client,
    token_model=OAuth2Token,
)
require_oauth = ResourceProtector()
authorization.register_grant(ClientCredentialsGrant)
authorization.register_client_auth_method(
    JWTClientAuth.CLIENT_AUTH_METHOD,
    JWTClientAuth(settings.AUTHORIZATION_SERVER_TOKEN_ENDPOINT_URI))
authorization.register_endpoint(ZoAuth2IntrospectionEndpoint)
require_oauth.register_token_validator(BearerTokenValidator(OAuth2Token))
