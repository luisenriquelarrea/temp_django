from django.contrib.auth.models import User
from rest_framework import serializers

from .models import AccionBasica

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

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]