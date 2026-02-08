from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Accion(models.Model):
    seccion_menu = models.ForeignKey(
        "SeccionMenu",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="acciones"
    )

    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    call_method = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    label = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    icon = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    on_breadcrumb = models.BooleanField(default=False)
    on_navbar = models.BooleanField(default=False)
    on_table = models.BooleanField(default=False)

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        related_name="acciones_creadas"
    )
    user_updated = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        related_name="acciones_actualizadas"
    )

    class Meta:
        db_table = "accion"
        verbose_name = "Acción"
        verbose_name_plural = "Acciones"

        constraints = [
            models.UniqueConstraint(
                fields=["seccion_menu", "descripcion"],
                name="accion_seccion_menu_id_descripcion_unique"
            )
        ]

    def __str__(self):
        return self.label or self.descripcion or f"Accion {self.id}"
class AccionBasica(models.Model):
    descripcion = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    call_method = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    label = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    icon = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    on_breadcrumb = models.BooleanField(default=False)
    on_navbar = models.BooleanField(default=False)
    on_table = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        related_name="acciones_basicas_creadas"
    )
    user_updated = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        null=True,
        related_name="acciones_basicas_actualizadas"
    )

    class Meta:
        db_table = "accion_basica"
        verbose_name = "Acción básica"
        verbose_name_plural = "Acciones básicas"

    def __str__(self):
        return self.descripcion or f"AccionBasica {self.id}"
    
class AccionGrupo(models.Model):
    accion = models.ForeignKey(
        "Accion",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="grupos_relacionados"
    )

    grupo = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="acciones_relacionadas"
    )

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="acciones_grupo_creadas"
    )

    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="acciones_grupo_actualizadas"
    )

    class Meta:
        db_table = "accion_grupo"
        verbose_name = "Acción por grupo"
        verbose_name_plural = "Acciones por grupo"

        constraints = [
            models.UniqueConstraint(
                fields=["accion", "grupo"],
                name="accion_grupo_accion_grupo_unique"
            )
        ]

    def __str__(self):
        return f"{self.accion} → {self.grupo}"
    
class Menu(models.Model):
    descripcion = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )
    label = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    icon = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    orden = models.IntegerField(
        null=True,
        blank=True
    )

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="menus_creados"
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="menus_actualizados"
    )

    class Meta:
        db_table = "menu"
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        ordering = ["orden"]

    def __str__(self):
        return self.label or self.descripcion or f"Menu {self.id}"

class SeccionMenu(models.Model):
    menu = models.ForeignKey(
        "Menu",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="secciones"
    )

    descripcion = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    navbar_label = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    icon = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    visible_app = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="secciones_menu_creadas"
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="secciones_menu_actualizadas"
    )

    class Meta:
        db_table = "seccion_menu"
        verbose_name = "Sección de menú"
        verbose_name_plural = "Secciones de menú"

    def __str__(self):
        return self.navbar_label or self.descripcion or f"SeccionMenu {self.id}"
    
class SeccionMenuInput(models.Model):
    seccion_menu = models.ForeignKey(
        "SeccionMenu",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="inputs"
    )

    input_type = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    input_label = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    input_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    input_name = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    input_cols = models.IntegerField(
        null=True,
        blank=True
    )

    input_required = models.BooleanField(default=False)

    input_accepts = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    keyboard_type = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    alta = models.BooleanField(default=False)
    modifica = models.BooleanField(default=False)
    lista = models.BooleanField(default=False)
    filtro = models.BooleanField(default=False)
    encabezado = models.BooleanField(default=False)
    new_line = models.BooleanField(default=False)
    currency_format = models.BooleanField(default=False)
    number_format = models.BooleanField(default=False)
    multiple = models.BooleanField(default=False)

    orden = models.IntegerField(
        null=True,
        blank=True
    )

    select_columnas = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    select_values = models.TextField(
        null=True,
        blank=True
    )

    select_filters = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    url_get = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    modelo = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="inputs_creados"
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="inputs_actualizados"
    )

    class Meta:
        db_table = "seccion_menu_input"
        verbose_name = "Input de sección de menú"
        verbose_name_plural = "Inputs de sección de menú"
        ordering = ["orden"]

    def __str__(self):
        return self.input_label or self.input_name or f"Input {self.id}"
    
class StyledColumn(models.Model):
    seccion_menu = models.ForeignKey(
        "SeccionMenu",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="styled_columns"
    )

    columna = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    valor = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    background_color = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    color = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    border = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="styled_columns_created"
    )

    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="styled_columns_updated"
    )

    class Meta:
        db_table = "styled_column"
        verbose_name = "Styled Column"
        verbose_name_plural = "Styled Columns"

        constraints = [
            models.UniqueConstraint(
                fields=["seccion_menu", "columna", "valor"],
                name="styled_column_seccion_menu_columna_valor_unique"
            )
        ]

        indexes = [
            models.Index(fields=["seccion_menu", "status"]),
        ]

    def __str__(self):
        return f"{self.seccion_menu_id} | {self.columna} = {self.valor}"