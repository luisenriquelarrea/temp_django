from django.contrib.auth.models import User

from rest_framework import permissions, viewsets

from .models import AccionBasica, Menu, SeccionMenu
from .serializers import AccionBasicaSerializer, MenuSerializer, SeccionMenuSerializer, UserSerializer

class AccionBasicaViewSet(viewsets.ModelViewSet):
    queryset = AccionBasica.objects.all()
    serializer_class = AccionBasicaSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class SeccionMenuViewSet(viewsets.ModelViewSet):
    queryset = SeccionMenu.objects.all()
    serializer_class = SeccionMenuSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]