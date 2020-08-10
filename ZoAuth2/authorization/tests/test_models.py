from django.test import TestCase
from authlib.jose import ECKey
from authorization.models import OAuth2Client
from .ClientTestCase import ClientTestCase

#PUBLIC_KEY_FILE = open('./public.pem', 'rb')
#PUBLIC_KEY = PUBLIC_KEY_FILE.read()
MEMO = (
    '2d2d2d2d2d424547494e205055424c4943204b45592d2d2'
    'd2d2d0a4d466b77457759484b6f5a497a6a304341515949'
    '4b6f5a497a6a304441516344516741455a6561524e58717'
    'a53727163696f31394a2b6a6577656a31615059390a4752'
    '563057724761732f6e33434a7359356a4c617968416f503'
    '633763073493043697635376d6b5a35496d393254483748'
    '4931366767672f57773d3d0a2d2d2d2d2d454e442050554'
    '24c4943204b45592d2d2d2d2d0a')


class TestOAuth2ClientModelManager(ClientTestCase):
    """TestOAuth2ClientModelManager."""

    def test_create_new_client(self):
        """test_create_new_client."""
        status = OAuth2Client.objects.create_client_or_update_scope(MEMO, 'PREMIUM')
        client = OAuth2Client.objects.get(public_key=bytes.fromhex(MEMO))
        self.assertEqual(client.scope, 'PREMIUM')
        self.assertEqual(status, True)

    def test_create_existing_client_with_same_scope(self):
        """test_create_existing_client_with_same_scope."""
        status = OAuth2Client.objects.create_client_or_update_scope(self.existing_memo, 'GOLD')
        self.assertEqual(status, False)

    def test_create_existing_client_and_update_scope(self):
        """test_create_existing_client_and_update_scope."""
        status = OAuth2Client.objects.create_client_or_update_scope(
            self.existing_memo, 'ONE_OFF_CONTENT')
        client = OAuth2Client.objects.get(public_key=bytes.fromhex(self.existing_memo))
        self.assertEqual(status, True)
        self.assertEqual(client.scope, 'GOLD ONE_OFF_CONTENT')


class TestOAuth2ClientModel(ClientTestCase):
    """TestOAuth2ClientModel."""

    def test_thumbprint_is_client_id(self):
        """test_thumbprint_is_client_id."""
        pubkey_bytes = bytes.fromhex(self.existing_memo)
        jwk = ECKey.import_key(pubkey_bytes)
        thumbprint = jwk.thumbprint()
        self.assertEqual(thumbprint, self.existing_client.get_client_id())

    def test_get_allowed_scopes(self):
        """test_get_allowed_scopes."""
        # add second scope
        OAuth2Client.objects.create_client_or_update_scope(
            self.existing_memo, 'ONE_OFF_CONTENT')

        client = OAuth2Client.objects.get(public_key=bytes.fromhex(self.existing_memo))
        allowed_scopes1 = client.get_allowed_scope('GOLD PLATINUM ONE_OFF_CONTENT')
        self.assertEqual(allowed_scopes1, 'GOLD ONE_OFF_CONTENT')
        allowed_scopes2 = client.get_allowed_scope('PLATINUM ONE_OFF_CONTENT')
        self.assertEqual(allowed_scopes2, 'ONE_OFF_CONTENT')
        allowed_scopes3 = client.get_allowed_scope('PLATINUM DIAMOND')
        self.assertEqual(allowed_scopes3, '')
