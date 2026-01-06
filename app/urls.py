from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from dashboard import views

router = routers.DefaultRouter()
router.register(r'accion_basica', views.AccionBasicaViewSet)
router.register(r"menu", views.MenuViewSet)
router.register(r"seccion_menu", views.SeccionMenuViewSet)
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/login/", views.LoginView.as_view(), name="login"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
]