from authlib.oauth2.rfc7523 import PrivateKeyJWT, private_key_jwt_sign
from authlib.oauth2.rfc6749 import grants

class ecdsaJWT(PrivateKeyJWT):
    name = 'ecdsa_key_jwt'

    def sign(self, auth, token_endpoint):
        return private_key_jwt_sign(
            auth.client_secret,
            client_id=auth.client_id,
            token_endpoint=token_endpoint,
            alg='ES256',
            claims=self.claims,
        )

class ClientCredentialsGrant(grants.ClientCredentialsGrant):
    TOKEN_ENDPOINT_AUTH_METHODS = [
        'ecdsa_key_jwt'
    ]


