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

def calcular_isr_determinado(isr, importe_gravado):
    """
    Calcula el ISR determinado conforme a la tarifa del Art. 96 de la LISR (México).

    Parámetros:
        isr: Objeto que representa el renglón de la tarifa aplicable, el cual contiene:
            - limite_inferior (Decimal): Límite inferior del rango
            - porcentaje_excedente (Decimal): Porcentaje aplicable sobre el excedente
            - cuota_fija (Decimal): Cuota fija correspondiente al rango
        importe_gravado (Decimal): Base gravable del periodo (ingreso gravado)

    Retorna:
        Decimal: ISR determinado redondeado a 2 decimales.
    """

    # Determinar el excedente sobre el límite inferior
    # Fórmula LISR:
    # Excedente = Base gravable - Límite inferior
    excedente = importe_gravado - isr.limite_inferior

    # Aplicar el porcentaje sobre el excedente
    # ISR sobre excedente = Excedente × (Porcentaje / 100)
    isr_excedente = excedente * isr.porcentaje_excedente / 100

    # Sumar la cuota fija establecida en la tarifa
    # ISR determinado = ISR sobre excedente + Cuota fija
    isr_determinado = isr_excedente + isr.cuota_fija

    # Redondear a 2 decimales conforme a práctica fiscal (moneda nacional)
    return isr_determinado.quantize(Decimal("0.01"))

def calcular_subsidio_empleo_causado(uma, periodicidad_pago):
    """
    Calcula el subsidio al empleo causado para un periodo específico
    según la nueva mecánica basada en porcentaje de UMA.

    :param uma: objeto UMA del ejercicio (contiene valor, factor_mensual y porcentaje_uma)
    :param periodicidad_pago: número de días del periodo (7=semanal, 15=quincenal, etc.)
    :return: subsidio al empleo causado para el periodo
    """

    # Convertir la UMA diaria a UMA mensual
    # (Ejemplo: UMA diaria * 30.4)
    uma_mensual = uma.valor * uma.factor_mensual

    # Calcular el subsidio mensual aplicando el porcentaje establecido por ley
    # (Ejemplo: UMA mensual * 15.02%)
    subsidio_mensual = uma_mensual * uma.porcentaje_uma

    # Obtener subsidio diario dividiendo entre el factor mensual (30.4)
    subsidio_diario = subsidio_mensual / uma.factor_mensual

    # Calcular subsidio causado para el periodo
    # (subsidio diario * número de días del periodo de pago)
    subsidio_empleo_causado = subsidio_diario * periodicidad_pago

    return subsidio_empleo_causado.quantize(Decimal("0.01"))

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
