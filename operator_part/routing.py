from django.urls import path

from .consumers import *

ws_urlpatterns = [
    path('ws/<int:pk>', WSConsumer.as_asgi())
]