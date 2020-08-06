from django.urls import path, include
from . import views

urlpatterns = [
    path('scan_transactions', views.scan_transactions, name='scan_transactions'),
]
