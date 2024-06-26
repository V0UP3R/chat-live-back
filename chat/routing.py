# chat/routing.py
from django.urls import path, re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path("ws/active_rooms/", consumers.ActiveRoomsConsumer.as_asgi()),
]