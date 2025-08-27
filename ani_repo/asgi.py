"""
ASGI config for ani_repo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ani_repo.settings')


from django.core.asgi import get_asgi_application #get asgi knows how to handle http request for the project
from channels.routing import ProtocolTypeRouter #Routes different types of connections (protocols) to the right handle
from channels.routing import URLRouter #Routes different types of connections (protocols) to the right handle
from animes import routing


application = ProtocolTypeRouter({ # to add different protocols and their handles
    'http': get_asgi_application(), #For HTTP requests, use Django’s usual ASGI app
    'websockets': URLRouter(routing.websocket_urlpatterns) #register paths list to URLRouter
})
