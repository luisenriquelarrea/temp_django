from django.db import models
from django.conf import settings

from nomina.services.nomina_math import (
    calcular_factor_integracion
)

from decimal import Decimal

class Plaza(models.Model):
    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True
    )

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="plazas_created"
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="plazas_updated"
    )

    class Meta:
        db_table = "plaza"
        verbose_name = "Plazas"
        verbose_name_plural = "Plazas"

    def __str__(self):
        return self.descripcion
    
class Departamento(models.Model):
    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="departments_created"
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="departments_updated"
    )

    class Meta:
        db_table = "departamento"
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.descripcion

class Empleado(models.Model):
    plaza = models.ForeignKey(
        "plaza",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="empleados"
    )

    departamento = models.ForeignKey(
        "departamento",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="empleados"
    )

    rfc = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    nombre_completo = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    sd = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal("0.00")
    )

    sdi = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal("0.00")
    )

    periodicidad_pago = models.IntegerField(
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
        related_name="employees_created"
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="employees_updated"
    )

    def save(self, *args, **kwargs):
        factor = calcular_factor_integracion()
        self.sdi = (self.sd * factor).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)

    class Meta:
        db_table = "empleado"
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        return self.rfc
    
class Nomina(models.Model):
    plaza = models.ForeignKey(
        "plaza",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="nominas"
    )

    departamento = models.ForeignKey(
        "departamento",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="nominas"
    )

    fecha = models.DateField()

    fecha_pago = models.DateField()

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="nominas_created"
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="nominas_updated"
    )

    class Meta:
        db_table = "nomina"
        verbose_name = "Nomina"
        verbose_name_plural = "Nominas"

    def __str__(self):
        return self.fecha

class Recibo(models.Model):
    nomina = models.ForeignKey(
        "nomina",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="recibos"
    )

    empleado = models.ForeignKey(
        "empleado",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="recibos"
    )

    sd = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal("0.00")
    )

    sdi = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal("0.00")
    )

    periodicidad_pago = models.IntegerField(
        null=True,
        blank=True
    )

    sueldos_salarios = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal("0.00")
    )

    isr_determinado = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal("0.00")
    )

    isr_pagar = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal("0.00")
    )

    subsidio_empleo_causado = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal("0.00")
    )

    subsidio_empleo_entregado = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal("0.00")
    )

    imss = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal("0.00")
    )

    neto = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal("0.00")
    )

    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="recibos_created"
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="recibos_updated"
    )

    class Meta:
        db_table = "recibo"
        verbose_name = "Recibo"
        verbose_name_plural = "Recibos"

    def __str__(self):
        return self.empleado