from django.urls import re_path
from gameLogic.consumers import WaitingRoomConsumer, GameRoomConsumer

websocket_urlpatterns = [
    re_path(r'ws/waiting/(?P<room_code>[^/]+)/$', WaitingRoomConsumer.as_asgi()),
        re_path(r'ws/game/(?P<room_code>[^/]+)/$', GameRoomConsumer.as_asgi()),
]