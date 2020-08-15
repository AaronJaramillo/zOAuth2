from django.test import TestCase, RequestFactory
from authlib.integrations.django_oauth2 import AuthorizationServer
from authorization.models import OAuth2Client, OAuth2Token
from .utils.utils import get_file_path

class AuthorizationServerTestCase(TestCase):
    @staticmethod
    def create_server():
        """create_server. Useful for creating a one off server object"""
        return AuthorizationServer(OAuth2Client, OAuth2Token)

    def setUp(self):
        self.factory = RequestFactory()


        public_key_file = open(get_file_path('public_key.pem'), 'rb')
        public_key = public_key_file.read()
        public_key_file.close()
        client = OAuth2Client(
            client_id='xx21',
            user_id='client',
            public_key=public_key,
            grant_type='client_credentials',
            scope='',
            token_endpoint_auth_method='ecdsa_key_jwt'

        )
        client.save()
