from django.db import transaction

from nomina.models import (
    Empleado,
    Recibo
)

from .nomina_math import (
    calcular_sueldos_salarios
)

@transaction.atomic
def process_nomina_detalle(nomina):
    empleados = Empleado.objects.filter(
        plaza=nomina.plaza,
        departamento=nomina.departamento,
        status=True
    )

    recibos = []

    for empleado in empleados:
        salario_diario = empleado.sd
        periodicidad_pago = empleado.periodicidad_pago

        if salario_diario == 0 or periodicidad_pago == 0:
            continue

        sueldos_salarios = calcular_sueldos_salarios(salario_diario, periodicidad_pago)

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
