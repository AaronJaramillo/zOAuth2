from django.test import TestCase, RequestFactory
from .ClientTestCase import ClientWithTokenTestCase
import base64
from authlib.common.encoding import to_bytes, to_unicode

def create_basic_auth(username, password):
    text = '{}:{}'.format(username, password)
    auth = to_unicode(base64.b64encode(to_bytes(text)))
    return 'Basic ' + auth


##TODO testTokenView(ClientTestCase):

class TestIntrospectionView(ClientWithTokenTestCase):
    """create_basic_auth.

    :param username:
    :param password:
    """
    def test_introspection_endpoint(self):
        """test_introspection_endpoint."""
        auth_header = create_basic_auth('resource', 'secret')

        response = self.client.post(
            '/authorization/introspection',
            {'token': self.token.access_token},
            HTTP_AUTHORIZATION=auth_header)
        self.assertEqual(response.json()['active'], True)
