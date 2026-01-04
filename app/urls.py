from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from dashboard import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r'accion_basica', views.AccionBasicaViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
]