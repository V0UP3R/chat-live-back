# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from .models import ActiveRoom

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.add_room()
        self.update_active_rooms()
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        self.remove_room()
        self.update_active_rooms()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))

    def update_active_rooms(self):
        channel_layer = get_channel_layer()
        active_rooms = list(ActiveRoom.objects.values_list('name', flat=True))
        async_to_sync(channel_layer.group_send)(
            "active_rooms", {"type": "active.rooms", "rooms": active_rooms}
        )

    def add_room(self):
        if not ActiveRoom.objects.filter(name=self.room_name).exists():
            ActiveRoom.objects.create(name=self.room_name)

    def remove_room(self):
        if not ActiveRoom.objects.filter(name=self.room_name).exists():
            ActiveRoom.objects.filter(name=self.room_name).delete()

class ActiveRoomsConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        active_rooms = list(ActiveRoom.objects.values_list('name', flat=True))
        self.send(text_data=json.dumps({"rooms": active_rooms}))
        async_to_sync(self.channel_layer.group_add)(
            "active_rooms", self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "active_rooms", self.channel_name
        )

    def active_rooms(self, event):
        rooms = event["rooms"]
        self.send(text_data=json.dumps({"rooms": rooms}))
