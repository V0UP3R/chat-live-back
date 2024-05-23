from .models import ActiveRoom
from django.http import JsonResponse
from django.shortcuts import render



def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


def active_rooms(request):
    rooms = list(ActiveRoom.objects.values_list('name', flat=True))
    return JsonResponse({'rooms': rooms})
