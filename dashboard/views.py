from django.contrib.auth.models import User

from rest_framework import permissions, viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from dashboard.services.accion_grupo_service import (
    get_allowed_breadcrumbs_for_group,
    get_allowed_menus_for_group,
    get_allowed_navbar_for_group,
    get_allowed_table_actions_for_group,
)

from .models import AccionBasica, AccionGrupo, Menu, SeccionMenu

from .serializers import (
    LoginSerializer, 
    AccionBasicaSerializer, 
    AccionGrupoSerializer,
    AccionGrupoActionsSerializer,
    AccionGrupoSeccionMenuSerializer,
    MenuSerializer, 
    SeccionMenuSerializer, 
    UserSerializer
)

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

class AccionGrupoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        accion_grupo = AccionGrupo.objects.all()

        serializer = AccionGrupoSerializer(accion_grupo, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="allowed_breadcrumbs")
    def allowed_breadcrumbs(self, request):
        seccion_menu_id = request.data.get("seccion_menu_id")

        if not seccion_menu_id:
            return Response(
                {"detail": "seccion_menu_id is required"},
                status=400
            )

        acciones = get_allowed_breadcrumbs_for_group(
            request.user,
            seccion_menu_id
        )

        serializer = AccionGrupoActionsSerializer(acciones, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["post"], url_path="allowed_navbar")
    def allowed_navbar(self, request):
        seccion_menu_id = request.data.get("seccion_menu_id")

        if not seccion_menu_id:
            return Response(
                {"detail": "seccion_menu_id is required"},
                status=400
            )

        acciones = get_allowed_navbar_for_group(
            request.user,
            seccion_menu_id
        )

        serializer = AccionGrupoActionsSerializer(acciones, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="allowed_menus")
    def allowed_menus(self, request):
        seccion_menus = get_allowed_menus_for_group(request.user)

        serializer = AccionGrupoSeccionMenuSerializer(seccion_menus, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["post"], url_path="allowed_table_actions")
    def allowed_table_actions(self, request):
        seccion_menu_id = request.data.get("seccion_menu_id")

        if not seccion_menu_id:
            return Response(
                {"detail": "seccion_menu_id is required"},
                status=400
            )

        acciones = get_allowed_table_actions_for_group(
            request.user,
            seccion_menu_id
        )

        serializer = AccionGrupoActionsSerializer(acciones, many=True)
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