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

def calcular_imss(salario_diario, periodicidad_pago, uma):
    """
    Calcula las cuotas obrero IMSS (trabajador) conforme a la LSS.

    Parámetros:
        salario_diario (Decimal): Salario diario del trabajador.
        periodicidad_pago (int): Días pagados en el periodo (ej. 15, 14, 7, 30).
        uma: Objeto que contiene el valor vigente de la UMA.

    Retorna:
        Decimal: Total de cuotas obreras IMSS del periodo.
    """

    # Calcular Salario Base de Cotización (Art. 27 LSS)
    sbc = calcular_salario_base_cotizacion(salario_diario, uma)

    imss = Decimal("0.00")

    # --------------------------------------------------------
    # Seguro de Enfermedades y Maternidad
    # --------------------------------------------------------

    # Prestaciones en especie
    # El trabajador paga 0.40% únicamente sobre el excedente
    # del SBC que supere 3 UMA (Art. 106 LSS)
    diferencia_3uma_sbc = sbc - (uma.valor * 3)

    if diferencia_3uma_sbc > 0:
        imss += (Decimal("0.40") / 100) * diferencia_3uma_sbc * periodicidad_pago

    # Gastos médicos para pensionados y beneficiarios
    # Cuota obrera: 0.375% sobre el SBC (Art. 107 LSS)
    imss += (Decimal("0.375") / 100) * sbc * periodicidad_pago

    # 2.3 Prestaciones en dinero
    # Cuota obrera: 0.25% sobre el SBC (Art. 107 LSS)
    imss += (Decimal("0.25") / 100) * sbc * periodicidad_pago

    # --------------------------------------------------------
    # Seguro de Invalidez y Vida
    # --------------------------------------------------------

    # En especie y dinero
    # Cuota obrera: 0.625% sobre el SBC (Art. 147 LSS)
    imss += (Decimal("0.625") / 100) * sbc * periodicidad_pago

    # --------------------------------------------------------
    # Retiro, Cesantía en Edad Avanzada y Vejez (CEAV)
    # --------------------------------------------------------

    # Cuota obrera Cesantía y Vejez: 1.125% sobre el SBC
    # (Art. 168 LSS)
    imss += (Decimal("1.125") / 100) * sbc * periodicidad_pago

    return imss.quantize(Decimal("0.01"))

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

    return isr_determinado.quantize(Decimal("0.01"))

def calcular_isr_retenido(isr_determinado, subsidio_causado):
    """
    Calcula el ISR a retener conforme a LISR considerando subsidio al empleo.

    Parámetros:
        isr_determinado (Decimal): ISR calculado conforme tarifa Art. 96 LISR.
        subsidio_causado (Decimal): Subsidio al empleo causado en el periodo.

    Retorna:
        dict con:
            - isr_retenido
            - subsidio_entregado
    """

    resultado = isr_determinado - subsidio_causado

    if resultado > 0:
        return {
            "isr_retenido": resultado.quantize(Decimal("0.01")),
            "subsidio_entregado": Decimal("0.00")
        }
    else:
        return {
            "isr_retenido": Decimal("0.00"),
            "subsidio_entregado": abs(resultado).quantize(Decimal("0.01"))
        }
    
def calcular_neto(
    percepciones_gravadas,
    percepciones_exentas,
    subsidio_empleo_entregado,
    isr_retenido,
    imss
):
    """
    Calcula el salario neto a pagar al trabajador.

    Fórmula conforme a práctica de nómina en México:

        Neto = Total percepciones
             + Subsidio al empleo entregado
             - ISR retenido
             - Cuotas obrero IMSS

    Parámetros:
        percepciones_gravadas (Decimal):
            Total de ingresos gravados del periodo.

        percepciones_exentas (Decimal):
            Total de ingresos exentos del periodo.

        subsidio_empleo_entregado (Decimal):
            Subsidio al empleo pagado en efectivo al trabajador
            cuando el subsidio causado es mayor que el ISR determinado.

        isr_retenido (Decimal):
            ISR efectivamente retenido (Art. 96 LISR).

        imss (Decimal):
            Total de cuotas obreras IMSS retenidas en el periodo.

    Retorna:
        Decimal: Importe neto a pagar, redondeado a 2 decimales.
    """

    # 1️⃣ Total de percepciones
    total_percepciones = percepciones_gravadas + percepciones_exentas

    # 2️⃣ Cálculo del neto
    neto = (
        total_percepciones
        + subsidio_empleo_entregado   # Se SUMA porque es ingreso
        - isr_retenido
        - imss
    )

    return neto.quantize(Decimal("0.01"))
    
def calcular_salario_base_cotizacion(
    salario_diario,
    uma,
    aguinaldo_dias=AGUINALDO_DIAS,
    vacaciones_dias=VACACIONES_DIAS,
    prima_vacacional=PRIMA_VACACIONAL,
):
    """
    Calcula el Salario Base de Cotización (SBC) conforme al Art. 27 de la Ley del Seguro Social.

    El SBC se integra con:
        - Salario diario
        - Parte proporcional de aguinaldo
        - Parte proporcional de prima vacacional

    Parámetros:
        salario_diario (Decimal): Salario diario nominal del trabajador.
        aguinaldo_dias (int): Días de aguinaldo otorgados al año.
        vacaciones_dias (int): Días de vacaciones otorgados al año.
        prima_vacacional (Decimal): Porcentaje de prima vacacional (ej. 0.25 para 25%).

    Retorna:
        Decimal: Salario Base de Cotización redondeado a 2 decimales.
    """

    # Parte proporcional diaria de aguinaldo
    # Fórmula:
    # (Días de aguinaldo × Salario diario) / 365
    proporcional_aguinaldo = (
        (aguinaldo_dias * salario_diario) / DIAS_ANIO
    )

    # Parte proporcional diaria de prima vacacional
    # Fórmula:
    # (Días de vacaciones × Salario diario × Prima vacacional) / 365
    proporcional_prima_vacacional = (
        (vacaciones_dias * salario_diario * prima_vacacional) / DIAS_ANIO
    )

    # Integración del SBC
    # SBC = Salario diario
    #     + Proporcional aguinaldo
    #     + Proporcional prima vacacional
    sbc = (
        salario_diario
        + proporcional_aguinaldo
        + proporcional_prima_vacacional
    )

    tope_sbc = uma.valor * 25
    if sbc > tope_sbc:
        sbc = tope_sbc

    return sbc.quantize(Decimal("0.01"))

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
    subsidio_mensual = uma_mensual * (uma.porcentaje_uma / 100)

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
