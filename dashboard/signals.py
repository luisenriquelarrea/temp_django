from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from .models import SeccionMenu, Accion, AccionBasica, AccionGrupo

@receiver(post_save, sender=Accion)
def create_accion_grupo(sender, instance, created, **kwargs):
    if created:
        grupo = Group.objects.get(name="administrador")

        AccionGrupo.objects.get_or_create(
            accion=instance,
            grupo=grupo
        )

@receiver(post_save, sender=SeccionMenu)
def create_default_acciones(sender, instance, created, **kwargs):
    if created:
        acciones_basicas = AccionBasica.objects.filter(
            status=True
        )

        for accion_basica in acciones_basicas:
            Accion.objects.get_or_create(
                seccion_menu=instance,
                descripcion=accion_basica.descripcion,
                call_method=accion_basica.call_method,
                label=accion_basica.label,
                icon=accion_basica.icon,
                on_breadcrumb=accion_basica.on_breadcrumb,
                on_navbar=accion_basica.on_navbar,
                on_table=accion_basica.on_table
            )
