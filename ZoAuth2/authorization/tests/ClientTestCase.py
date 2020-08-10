from django.test import TestCase
from authorization.models import OAuth2Client


class ClientTestCase(TestCase):
    """ClientTestCase."""

    def setUp(self):
        """setUp."""
        self.existing_memo = (
            '2d2d2d2d2d424547494e205055424c4943204b45592d2d2d'
            '2d2d0a4d466b77457759484b6f5a497a6a3043415159494b'
            '6f5a497a6a304441516344516741456d5a47624b36664254'
            '676163735a50476c6a78547555344272474c370a4b575466'
            '5059683154696c454d746872533566597970413144417247'
            '62694f2b6f2f656a4d645877616e68714c396a4564573974'
            '6b68414656673d3d0a2d2d2d2d2d454e44205055424c4943'
            '204b45592d2d2d2d2d0a')
        OAuth2Client.objects.create_client_or_update_scope(
            self.existing_memo, 'GOLD')
        self.existing_client = OAuth2Client.objects.get(
            public_key=bytes.fromhex(self.existing_memo))
