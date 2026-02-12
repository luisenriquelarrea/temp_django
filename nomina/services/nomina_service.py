from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from nomina.models import (
    Empleado,
    Recibo,
    IsrSemanal,
    IsrQuincenal,
    Uma
)

from .nomina_math import (
    calcular_isr_determinado,
    calcular_isr_retenido,
    calcular_sueldos_salarios,
    calcular_subsidio_empleo_causado
)

def get_isr(ejercicio, sueldos_salarios, periodicidad_pago):
    model = {
        7: IsrSemanal,
        15: IsrQuincenal
    }.get(periodicidad_pago)

    if not model:
        raise ValueError(f"ISR model not found for periodicidad_pago {periodicidad_pago}")

    isr = model.objects.filter(
        ejercicio=ejercicio,
        status=True,
        limite_inferior__lte=sueldos_salarios
    ).filter(
        Q(limite_superior__gte=sueldos_salarios) |
        Q(limite_superior__isnull=True)
    ).order_by('limite_inferior').first()

    if not isr:
        raise ValueError(f"ISR record not found")
    
    return isr

def get_uma(ejercicio):
    uma = Uma.objects.filter(
        ejercicio=ejercicio,
        status=True
    ).first()

    if not uma:
        raise ValueError(f"UMA not found for ejercicio {ejercicio}")
    
    return uma

@transaction.atomic
def process_nomina_detalle(nomina):
    empleados = Empleado.objects.filter(
        plaza=nomina.plaza,
        departamento=nomina.departamento,
        status=True
    )

    ejercicio = timezone.now().year

    uma = get_uma(ejercicio)

    recibos = []

    for empleado in empleados:
        salario_diario = empleado.sd
        periodicidad_pago = empleado.periodicidad_pago

        if salario_diario == 0 or periodicidad_pago == 0:
            continue

        sueldos_salarios = calcular_sueldos_salarios(salario_diario, periodicidad_pago)

        subsidio_empleo_causado = 0

        if sueldos_salarios <= uma.limite_max:
            subsidio_empleo_causado = calcular_subsidio_empleo_causado(uma, periodicidad_pago)

        isr = get_isr(ejercicio, sueldos_salarios, periodicidad_pago)

        isr_determidado = calcular_isr_determinado(isr, sueldos_salarios)

        tmp = calcular_isr_retenido(isr_determidado, subsidio_empleo_causado)

        isr_retenido = tmp.get("isr_retenido")

        subsidio_empleo_entregado = tmp.get("subsidio_entregado")

        recibos.append(
            Recibo(
                nomina=nomina,
                empleado=empleado,
                periodicidad_pago=periodicidad_pago,
                sd=salario_diario,
                sdi=empleado.sdi,
                sueldos_salarios=sueldos_salarios,
            )
        )

    Recibo.objects.bulk_create(recibos)
