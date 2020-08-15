from django.shortcuts import render
from django.http import JsonResponse
from django_q.tasks import async_task
# Create your views here.

def block_notify(request):
    """block_notify.

    :param request:
    """
    async_task('registration.tasks.query_transactions')
    return JsonResponse({"Transactions": "Qeuried"})

