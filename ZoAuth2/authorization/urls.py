from django.urls import path, include
from . import views

urlpatterns = [
    path('token', views.issue_token, name='issue_token'),
    path('introspection', views.introspect_token, name="introspect_token")
]
