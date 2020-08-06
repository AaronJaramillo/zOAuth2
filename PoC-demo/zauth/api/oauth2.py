from authlib.integrations.django_oauth2 import AuthorizationServer, ResourceProtector, BearerTokenValidator
from api.models import OAuth2Client, OAuth2Token
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc7523 import PrivateKeyJWT, private_key_jwt_sign, JWTBearerClientAssertion
from .models import OAuth2Client, OAuth2Token
from authlib.jose import ECKey

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zauth.settings')

class ecdsaJWT(PrivateKeyJWT):

    name = 'ecdsa_key_jwt'

    def sign(self, auth, token_endpoint):
        return private_key_jwt_sign(
            auth.client_secret,
            client_id=auth.client_id,
            token_endpoint = token_endpoint,
            alg='ES256',
            claims=self.claims,
        )

class JWTClientAuth(JWTBearerClientAssertion):
    CLIENT_AUTH_METHOD = 'ecdsa_key_jwt'
    def validate_jti(self, claims, jti):
        key = 'jti:{}-{}'.format(claims['sub'], jti)
        print(key)
        return True

    def resolve_client_public_key(self, client, headers):
        return client.public_key
        #key_dict = {'crv': 'P-256', 'x': 'q0YLj5TppHQplEX3RaZoN3Eii9ihPocZakbUnuU6Zsw', 'y': 'J1Ijhh7H0TWveNjBpMhylNlZlTDsX50KXUanIJJd3Ks', 'kty': 'EC'}
        #return ECKey.import_key(key_dict)

class ClientCredentialsGrant(grants.ClientCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'ecdsa_key_jwt'
    ]

#def create_query_client_func(client_model):
#    def query_client(client_id):
#        return client_model.objects.get(client_id=client_id).first()
#    return query_client
#
#def create_save_token_func(token_model):
#    def save_token(token, request):
#        client = request.client
#        item = token_model(
#            client_id=client.client_id,
#            user_id=user_id,
#            **token
#        )
#        item.save()
#    return save_token

#query_client = create_query_client_func(OAuth2Client)
#save_token = create_save_token_func(OAuth2Token)
authorization = AuthorizationServer(
    client_model=OAuth2Client,
    token_model=OAuth2Token,
)
require_oauth = ResourceProtector()
authorization.register_grant(ClientCredentialsGrant)
authorization.register_client_auth_method(JWTClientAuth.CLIENT_AUTH_METHOD, JWTClientAuth('http://127.0.0.1:8000/api/token'))
require_oauth.register_token_validator(BearerTokenValidator(OAuth2Token))
