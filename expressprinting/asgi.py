"""
ASGI config for expressprinting project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from operator_part.routing import ws_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expressprinting.settings')

application = get_asgi_application()#ProtocolTypeRouter({
    #'http': ,
    # 'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns))
#})
