# views.py
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'

    def perform_destroy(self, instance):
        instance.userprofile.is_deleted = True
        instance.userprofile.save()

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]