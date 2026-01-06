from django.contrib.auth.models import User

from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import AccionBasica, Menu, SeccionMenu
from .serializers import LoginSerializer, AccionBasicaSerializer, MenuSerializer, SeccionMenuSerializer, UserSerializer

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.validated_data

        return Response({
            "user": user_data
        })
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