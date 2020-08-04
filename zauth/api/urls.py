from django.urls import path, include
from . import views

urlpatterns = [
    path('get_products', views.get_products, name='get_products'),
    path('create_client', views.create_client, name='create_client'),
    path('token', views.issue_token, name='issue_token'),
    path('premium', views.premium, name='premium'),
    path('create_product', views.create_product, name='create_product')
]
