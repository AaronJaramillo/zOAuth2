from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .ZoAuth2Server import authorization

# Create your views here.

@csrf_exempt
def issue_token(request):
    """issue_token.

    :param request:
    """
    return authorization.create_token_response(request)
