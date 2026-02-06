from django.contrib.auth.models import User

from rest_framework import permissions, viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from dashboard.services.accion_grupo_service import (
    get_allowed_menus_for_user
)

from .models import AccionBasica, Menu, SeccionMenu
from .serializers import (LoginSerializer, AccionBasicaSerializer, AccionGrupoSerializer, 
                          MenuSerializer, SeccionMenuSerializer, UserSerializer)

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

class AccionGrupoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="allowed_menus")
    def allowed_menus(self, request):
        acciones = get_allowed_menus_for_user(request.user)

        serializer = AccionGrupoSerializer(acciones, many=True)
        return Response(serializer.data)

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