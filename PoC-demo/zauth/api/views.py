from django.shortcuts import render
from werkzeug.security import gen_salt
from django.http import JsonResponse
from .models import OAuth2Client
from backend.models import Product
from .oauth2 import authorization, require_oauth
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.

@csrf_exempt
def create_product(request):
    product = Product(
        name=request.POST.get('name'),
        address=request.POST.get('address'),
        period=datetime.timedelta(int(request.POST.get('period'))),
        scope=request.POST.get('scope'),
        price=int(request.POST.get('price'))
    )
    product.save()
    return JsonResponse({'name': product.name, 'address': product.address, 'price': product.price})

def get_products(request):
    products = Product.objects.all()
    return JsonResponse([{'address': product.address, 'price': product.price, 'scope': product.scope} for product in products], safe=False)

def create_client(request):
    print('client is creatings')

    client_id = gen_salt(24)
    client = OAuth2Client(
        client_id=client_id,
        user_id=client_id,
        redirect_uris='https://home.com',
        scope='premium',
        response_type='home',
        grant_type='client_credentials',
        token_endpoint_auth_method='ecdsa_key_jwt'
    )
    client.save()
    return JsonResponse({'client_id': client_id})

## TOken endpoint
    #authorization.create_token_response()
@csrf_exempt
def issue_token(request):
    return authorization.create_token_response(request)

@require_oauth('premium')
def premium(request):
    return JsonResponse({"this shit": "Is Premium"})
