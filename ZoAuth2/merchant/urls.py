from django.urls import path, include
from . import views

app_name = 'merchant'

urlpatterns = [
    path('product/', views.create_product, name='create_product'),
    path('get_products', views.get_products, name='get_products'),
    path("register/", views.register, name="register"),
    path('login', views.login_request, name="login"),
    path('dashboard', views.DashboardView.as_view(), name="dashboard"),
    path('createproduct', views.CreateProductView.as_view(), name="createproduct")
]
