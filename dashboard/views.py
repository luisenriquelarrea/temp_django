from django.contrib.auth.models import User

from rest_framework import permissions, viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import AccionGrupo

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
        user = request.user

        grupos = user.groups.all()

        acciones = AccionGrupo.objects.filter(
            grupo__in=grupos,
            status=True,
            accion__status=True
        ).select_related(
            "accion",
            "accion__seccion_menu",
            "accion__seccion_menu__menu"
        )

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