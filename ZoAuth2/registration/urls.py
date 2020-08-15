from django.urls import path, include
from . import views

urlpatterns = [
    path('block', views.block_notify, name='block_notify'),
]
