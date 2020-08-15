from django.urls import path, include
from . import views

urlpatterns = [
    path('product/', views.create_product, name='create_product'),
    path('get_products', views.get_products, name='get_products')
]
