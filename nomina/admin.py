from django.contrib import admin

from .models import (
    Plaza,
    Departamento,
    Empleado,
    Nomina,
    Recibo
)

@admin.register(Plaza)
class PlazaAdmin(admin.ModelAdmin):
    list_display = (
        "descripcion",
        "status",
    )

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = (
        "descripcion",
        "status",
    )

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        "plaza",
        "departamento",
        "nombre_completo",
        "rfc",
        "sd",
        "sdi",
        "status",
    )
    exclude = ("sdi",)

@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = (
        "plaza",
        "departamento",
        "fecha",
        "fecha_pago",
        "status",
    )

@admin.register(Recibo)
class ReciboAdmin(admin.ModelAdmin):
    list_display = (
        "nomina",
        "empleado",
        "periodicidad_pago",
        "sd",
        "sdi",
        "sueldos_salarios",
        "isr_determinado",
        "isr_pagar",
        "subsidio_empleo_causado",
        "subsidio_empleo_entregado",
        "imss",
        "neto"
    )