import os
import json
from authorization.ZoAuth2Server import authorization
from authorization.ZoAuth2Server import ecdsaJWT
from .AuthServerTestCase import AuthorizationServerTestCase
from .utils.utils import read_file_path
from .OAuth2SessionFactory import OAuth2SessionFactory

os.environ['AUTHLIB_INSECURE_TRANSPORT'] = 'true'

class TestTokenResponseEndpoint(AuthorizationServerTestCase):
    def test_client_credentials_ecdsa_jwt_auth(self):
        client_id = 'xx21'
        client_secret = read_file_path('private_key.json')
        token_endpoint = 'http://127.0.0.1:8000/authorization/token'

        session = OAuth2SessionFactory(
            client_id,
            client_secret,
            token_endpoint_auth_method='ecdsa_key_jwt',
            scope=''
        )
        session.register_client_auth_method(ecdsaJWT(token_endpoint))
        token_request = session.fetch_access_token(
            token_endpoint, grant_type='client_credentials')

        resp = authorization.create_token_response(token_request)
        self.assertIn('access_token', json.loads(resp.content))
