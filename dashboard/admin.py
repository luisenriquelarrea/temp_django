from django.contrib import admin
from .models import (
    AccionBasica,
    Accion,
    AccionGrupo,
    Menu,
    SeccionMenu,
    SeccionMenuInput,
)

@admin.register(AccionBasica)
class AccionBasicaAdmin(admin.ModelAdmin):
    list_display = (
        "descripcion",
        "label",
        "icon",
        "on_breadcrumb",
        "on_navbar",
        "on_table",
        "status",
    )

@admin.register(Accion)
class AccionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "seccion_menu",
        "descripcion",
        "label",
        "icon",
        "on_breadcrumb",
        "on_navbar",
        "on_table",
        "status",
    )

@admin.register(AccionGrupo)
class AccionGrupoAdmin(admin.ModelAdmin):
    list_display = (
        "grupo",
        "get_seccion_menu",
        "accion",
        "status",
    )

    def get_seccion_menu(self, obj):
        return obj.accion.seccion_menu

    get_seccion_menu.short_description = "Sección menú"

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "descripcion",
        "label",
        "icon",
        "orden",
        "status",
    )

@admin.register(SeccionMenu)
class SeccionMenuAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "menu",
        "descripcion",
        "navbar_label",
        "icon",
        "status",
    )

@admin.register(SeccionMenuInput)
class SeccionMenuInputAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "seccion_menu",
        "input_type",
        "input_label",
        "input_id",
        "input_name",
        "orden",
        "status",
    )

# admin.site.register(StyledColumn)