from decimal import Decimal

# === Constantes (LFT / IMSS) ===
AGUINALDO_DIAS = Decimal("15")        # Aguinaldo mínimo por ley
VACACIONES_DIAS = Decimal("12")       # Vacaciones 1er año (LFT 2023+)
PRIMA_VACACIONAL = Decimal("0.25")    # 25% mínimo legal
DIAS_ANIO = Decimal("365")            # Días del año usados por IMSS


def calcular_factor_integracion(
    aguinaldo_dias=AGUINALDO_DIAS,
    vacaciones_dias=VACACIONES_DIAS,
    prima_vacacional=PRIMA_VACACIONAL,
):
    """
    Calcula el Factor de Integración para el Salario Diario Integrado (SDI).

    Fórmula oficial IMSS:
        Factor = (365 + Aguinaldo + (Vacaciones × Prima Vacacional)) / 365

    Donde:
        - Aguinaldo: días de aguinaldo otorgados al trabajador
        - Vacaciones: días de vacaciones anuales
        - Prima Vacacional: porcentaje de la prima (ej. 0.25 = 25%)

    El factor se multiplica por el Salario Diario (SD) para obtener el SDI:

        SDI = SD × Factor

    Este factor:
        - Siempre es ≥ 1
        - Se recalcula cuando cambian prestaciones o antigüedad
        - Es utilizado exclusivamente para cálculos IMSS
    """

    # Prestaciones integrables:
    #  - Aguinaldo completo
    #  - Prima vacacional aplicada solo a días de vacaciones
    prestaciones = (
        aguinaldo_dias
        + (vacaciones_dias * prima_vacacional)
    )

    # Suma de días base del año + prestaciones
    dias_integrados = DIAS_ANIO + prestaciones

    # Factor de integración final
    factor_integracion = dias_integrados / DIAS_ANIO

    return factor_integracion

def calcular_sueldos_salarios(salario_diario, n_dias_pagados):
    """
    Calcula el importe de sueldos y salarios del periodo.

    Fórmula:
        sueldo_periodo = salario_diario × número_de_días_pagados

    Donde:
    - salario_diario: Salario diario del empleado (Decimal)
    - n_dias_pagados: Días pagados en el periodo de nómina (int o Decimal)

    El resultado se redondea a 2 decimales para cumplir con
    reglas contables y fiscales (centavos).
    """
    
    return (salario_diario * n_dias_pagados).quantize(Decimal("0.01"))
