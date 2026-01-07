from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User

from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Accion, AccionBasica, AccionGrupo, Menu, SeccionMenu

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data["username"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "groups": GroupSerializer(
                    user.groups.all(), many=True
                ).data
            }
        }

class AccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accion
        fields = "__all__"
        read_only_fields = [
            "created_at", "updated_at",
            "user_created_id", "user_updated_id"
        ]

class AccionBasicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccionBasica
        fields = [
            "id", "descripcion", "call_method", "label", "icon",
            "on_breadcrumb", "on_navbar", "on_table", "status",
            "created_at", "updated_at",
            "user_created_id", "user_updated_id"
        ]
        read_only_fields = [
            "created_at", "updated_at",
            "user_created_id", "user_updated_id"
        ]
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "id", "descripcion", "label", "icon", "orden",
            "status", "created_at", "updated_at",
            "user_created_id", "user_updated_id"
        ]
        read_only_fields = [
            "created_at", "updated_at",
            "user_created_id", "user_updated_id"
        ]

class SeccionMenuSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(read_only=True)
    class Meta:
        model = SeccionMenu
        fields = [
            "id", "menu", 
            "descripcion", "navbar_label", "icon",
            "status", "created_at", "updated_at",
            "user_created_id", "user_updated_id"
        ]
        read_only_fields = [
            "created_at", "updated_at",
            "user_created_id", "user_updated_id"
        ]
class AccionGrupoSerializer(serializers.ModelSerializer):
    seccionMenu = SeccionMenuSerializer(
        source="accion.seccion_menu",
        read_only=True
    )

    class Meta:
        model = AccionGrupo
        fields = ["id", "seccionMenu"]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]