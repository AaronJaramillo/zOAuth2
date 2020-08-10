#import time
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from authlib.oauth2.rfc6749.models import ClientMixin, TokenMixin
from authlib.jose import ECKey


# Create your models here.

class OAuth2ClientManager(models.Manager):
    """OAuth2ClientManager."""


    def create_client_or_update_scope(self, memo, scope):
        """get_or_create_client.

        :param memo:
        :param scope:
        """
        """get_or_create_client.

        :param memo: The hex encoded memo representing a public key
        :param scope: The purchased scope to grant access to
        """
        public_key = bytes.fromhex(memo)
        client_id = ECKey.import_key(public_key).thumbprint()
        token_endpoint_auth_method = 'ecdsa_key_jwt'
        grant_type = 'client_credentials'
        scope = scope
        client, created = self.get_or_create(
            client_id=client_id,
            user_id=client_id,
            public_key=public_key,
            token_endpoint_auth_method=token_endpoint_auth_method,
            grant_type=grant_type
        )
        if created:
            client.scope = scope
            client.save()
            return True
        return client.create_or_update_scope(scope)

        #redirect_uris
        #default_redirect_uri
        #response_type





class OAuth2Client(models.Model, ClientMixin):
    """OAuth2Client."""

    client_id = models.CharField(max_length=43, unique=True, db_index=True)
    user_id = models.CharField(max_length=43)
    client_name = models.CharField(max_length=120, blank=True)
    redirect_uris = models.TextField(default='')
    default_redirect_uri = models.TextField(blank=False, default='')
    scope = models.TextField(default='')
    response_type = models.TextField(default='')
    grant_type = models.TextField(default='')
    token_endpoint_auth_method = models.CharField(max_length=20, default='')
    public_key = models.BinaryField()
    objects = OAuth2ClientManager()

    def get_client_id(self):
        """get_client_id."""
        return self.client_id

    def get_default_redirect_uri(self):
        return self.default_redirect_uri

    def create_or_update_scope(self, scope):
        """create_or_update_scope.

        :param scope:
        """
        if scope in self.scope.split():
            # TODO handle client overpayments/double payments
            print('client already exists with scope')
            return False
        self.scope = self.scope + ' ' + scope
        self.save()
        return True

    @staticmethod
    def list_to_scope(scope_list):
        """list_to_scope.

        :param scope_list:
        """
        scopes = ''
        for scope in scope_list:
            if scopes == '':
                scopes = scope
                continue
            scopes = scopes + ' ' + scope
        return scopes

    def get_allowed_scope(self, scope):
        if not scope:
            return ''
        allowed = set(self.scope.split())
        return self.list_to_scope([s for s in scope.split() if s in allowed])

    def check_redirect_uri(self, redirect_uri):
        if redirect_uri == self.default_redirect_uri:
            return True
        return redirect_uri in self.redirect_uris

    def has_client_secret(self):
        return bool(self.client_secret)

    def check_token_endpoint_auth_method(self, method):
        return self.token_endpoint_auth_method == method

    def check_response_type(self, response_type):
        allowed = str(self.response_type).split()
        return response_type in allowed

    def check_grant_type(self, grant_type):
        allowed = str(self.grant_type).split()
        return grant_type in allowed
