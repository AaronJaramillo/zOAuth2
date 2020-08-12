from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .ZoAuth2Server import authorization, ZoAuth2IntrospectionEndpoint

# Create your views here.

@csrf_exempt
def issue_token(request):
    """issue_token.

    :param request:
    """
    return authorization.create_token_response(request)

@csrf_exempt
def introspect_token(request):
    """introspect_token."""
    return authorization.create_endpoint_response(ZoAuth2IntrospectionEndpoint.ENDPOINT_NAME, request)
