from django.db import models
from authlib.oauth2.rfc6749.models import ClientMixin
from authlib.oauth2.rfc6749.models import TokenMixin
from authlib.jose import ECKey
from django.core.exceptions import ObjectDoesNotExist
import time

def now_timestamp():
    return int(time.time())

# Create your models here.
class OAuth2ClientManager(models.Manager):
    def create_or_update_scope(self, memo, scope):
        try:
            client = self.get(public_key=bytes.fromhex(memo))
            if client.scope == scope:
                print('Scope already registered')
                return False
            else:
                client.scope = client.scope + ',' + scope
                client.save()
                return True
        except ObjectDoesNotExist:
            return self.create_client(memo, scope)


    def create_client(self, memo, scope):
        public_key = bytes.fromhex(memo)
        client_id = ECKey.import_key(public_key).thumbprint()
        token_endpoint_auth_method = 'ecdsa_key_jwt'
        grant_type = 'client_credentials'
        scope = scope

        #redirect_uris
        #default_redirect_uri
        #response_type

        client = OAuth2Client(
            client_id=client_id,
            user_id=client_id,
            public_key=public_key,
            token_endpoint_auth_method=token_endpoint_auth_method,
            grant_type=grant_type,
            scope=scope
        )
        client.save()
        return True


class OAuth2Client(models.Model, ClientMixin):
    client_id = models.CharField(max_length=48, unique=True, db_index=True)
    user_id = models.CharField(max_length=48)
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
        return self.client_id

    def get_default_redirect_uri(self):
        return self.default_redirect_uri

    def get_allowed_scope(self, scope):
        if not scope:
            return ''
        return self.scope

    def check_redirect_uri(self, redirect_uri):
        if redirect_uri == self.default_redirect_uri:
            return True
        return redirect_uri in self.redirect_uris

    def has_client_secret(self):
        return bool(self.client_secret)

    def check_client_secret(self, client_secret):
        return self.client_secret == client_secret

    def check_token_endpoint_auth_method(self, method):
        return self.token_endpoint_auth_method == method

    def check_response_type(self, response_type):
        allowed = self.response_type.split()
        return response_type in allowed

    def check_grant_type(self, grant_type):
        allowed = self.grant_type.split()
        return grant_type in allowed

class OAuth2Token(models.Model, TokenMixin):
    client_id  = models.CharField(max_length=48, db_index=True)
    user_id = models.CharField(max_length=48)
    token_type = models.CharField(max_length=40)
    access_token = models.CharField(max_length=255, unique=True, null=False)
    refresh_token = models.CharField(max_length=255, db_index=True)
    scope = models.TextField(default='')
    revoked = models.BooleanField(default=False)
    issued_at = models.IntegerField(null=False, default=now_timestamp)
    expires_in = models.IntegerField(null=False, default=0)

    def get_client_id(self):
        return self.client_id

    def get_scope(self):
        return self.scope

    def get_expires_in(self):
        return self.expires_in

    def get_expires_at(self):
        return self.issued_at + self.expires_in

