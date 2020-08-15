from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from registration.models import Product
import datetime
# Create your views here.

@csrf_exempt
def create_product(request):
    product = Product(
        name=request.POST.get('name'),
        address=request.POST.get('address'),
        period=datetime.timedelta(int(request.POST.get('period'))),
        scope=request.POST.get('scope'),
        price=int(request.POST.get('price')),
    )
    product.save()
    return JsonResponse({'product': product.name})

def get_products(request):
    products = Product.objects.all()
    return JsonResponse([{
        'address': product.address,
        'price': product.price,
        'scope': product.scope} for product in products], safe=False)
