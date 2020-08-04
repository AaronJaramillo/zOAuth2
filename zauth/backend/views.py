from django.shortcuts import render
from . import tasks
from django.http import JsonResponse

# Create your views here.

def scan_transactions(request):
    tasks.query_transactions.delay()
    return JsonResponse({'transactions scanning': 'yes'})
