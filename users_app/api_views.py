from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserSerializer


class UserCreate(generics.CreateAPIView):
    """
    Endpoint to create new User instance.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
