"""Implments a django.test request factory for use with the authlib.integrations.requsts_client Auth2Session authentication flow"""

from urllib import parse
from requests.sessions import Session, Request
from requests.auth import AuthBase
from authlib.integrations.requests_client import OAuth2Auth
from authlib.oauth2 import OAuth2Client as _OAuth2Client
from authlib.oauth2.auth import ClientAuth, TokenAuth
from django.test import RequestFactory

DEFAULT_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

class OAuth2ClientAuth(AuthBase, ClientAuth):
    """OAuth2ClientAuth."""

    """Attaches OAuth Client Authentication to the given Request object.
    """
    def __call__(self, req):
        req.url, req.headers, req.body = self.prepare(
            req.method, req.url, req.headers, req.body
        )
        return req

class SessionFactory(Session):
    """SessionFactory.
        Class overides requests.sessions Session.request method to return the PreparedRequest object instead of attempting to send it. useful for testing with django.test client
    """

    def request(
            self, method, url, params=None, data=None, headers=None, cookies=None, files=None,
            auth=None, timeout=None, allow_redirects=True, proxies=None,
            hooks=None, stream=None, verify=None, cert=None, json=None):

        # Create the Request.
        req = Request(
            method=method.upper(),
            url=url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks,
        )
        prep = self.prepare_request(req)

        proxies = proxies or {}

        settings = self.merge_environment_settings(
            prep.url, proxies, stream, verify, cert
        )

        return prep

class OAuth2Client(_OAuth2Client):
    """OAuth2Client. overrides the OAuth2Client class to return the fully formed fetch_token request with attempting to send it to the endpoint"""



    def _fetch_token(
            self, url, body='', headers=None,
            auth=None, method='POST', **kwargs):
        """_fetch_token. overrides the _fetch_token method to take the PreparedRequest and convert it to a RequestFactory POST request and return it it without sending to the endpoint. TODO: implement the logic for GET requests. NOTE: this whole factory may be surpurfulous but I couldn't make the authentication payload work any othe way for some reason

        :param url:
        :param body:
        :param headers:
        :param auth:
        :param method:
        :param kwargs:
        """

        if method == 'GET':
            if '?' in url:
                url = '&'.join([url, body])
            else:
                url = '?'.join([url, body])
            body = ''

        if headers is None:
            headers = DEFAULT_HEADERS

        req = self.session.request(
            method, url, data=body, headers=headers, auth=auth, **kwargs)

        path = parse.urlsplit(url).path
        req_data = parse.parse_qs(req.body)
        factory_req = RequestFactory().post(path, data=req_data)

        return factory_req

## Rewrite: OAuth2SessionFactory(OAuth2ClientMock, SessionFactory)
class OAuth2SessionFactory(OAuth2Client, SessionFactory):
    """OAuth2SessionFactory. Reimplements authlib.integrations.requests_client OAuth2Session class to use the overriden OAuth2Client and SessionFactory class thus returning django.tests.RequestFactory object instead of calling the endpoint and returning a response. """


    client_auth_class = OAuth2ClientAuth
    token_auth_class = OAuth2Auth

    SESSION_REQUEST_PARAMS = (
        'allow_redirects', 'timeout', 'cookies', 'files',
        'proxies', 'hooks', 'stream', 'verify', 'cert', 'json'
    )

    def __init__(self, client_id=None, client_secret=None,
                 token_endpoint_auth_method=None,
                 revocation_endpoint_auth_method=None,
                 scope=None, redirect_uri=None,
                 token=None, token_placement='header',
                 update_token=None, **kwargs):

        SessionFactory.__init__(self)
        OAuth2Client.__init__(
            self, session=self,
            client_id=client_id, client_secret=client_secret,
            token_endpoint_auth_method=token_endpoint_auth_method,
            revocation_endpoint_auth_method=revocation_endpoint_auth_method,
            scope=scope, redirect_uri=redirect_uri,
            token=token, token_placement=token_placement,
            update_token=update_token, **kwargs
        )

    def fetch_access_token(self, url=None, **kwargs):
        return self.fetch_token(url, **kwargs)

