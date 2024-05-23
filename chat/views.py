# chat/views.py
from django.http import JsonResponse
from django.shortcuts import render

from chat.consumers import ChatConsumer


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

def active_rooms(request):
    active_rooms = ChatConsumer.get_active_rooms()
    return JsonResponse({'active_rooms': active_rooms})