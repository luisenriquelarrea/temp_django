from django.contrib import admin

from nomina.services.nomina_service import process_nomina_detalle

from .models import (
    Plaza,
    Departamento,
    Empleado,
    Nomina,
    Recibo,
    IsrSemanal,
    IsrQuincenal,
    Uma
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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            process_nomina_detalle(obj)

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

@admin.register(IsrSemanal)
class IsrSemanalAdmin(admin.ModelAdmin):
    list_display = (
        "ejercicio",
        "limite_inferior",
        "limite_superior",
        "cuota_fija",
        "porcentaje_excedente",
        "status"
    )

@admin.register(IsrQuincenal)
class IsrQuincenalAdmin(admin.ModelAdmin):
    list_display = (
        "ejercicio",
        "limite_inferior",
        "limite_superior",
        "cuota_fija",
        "porcentaje_excedente",
        "status"
    )

@admin.register(Uma)
class UmaAdmin(admin.ModelAdmin):
    list_display = (
        "ejercicio",
        "valor",
        "porcentaje_uma",
        "factor_mensual",
        "status"
    )