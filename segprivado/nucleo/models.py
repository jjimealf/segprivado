from django.conf import settings
from django.db import models

from users.models import User


Usuario = User


class Cita(models.Model):
    fecha = models.DateField(null=True)
    observaciones = models.TextField(max_length=200, null=True)
    idMedico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="medico",
    )
    idPaciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="paciente",
    )

    class Meta:
        ordering = ("fecha",)


class Medicamento(models.Model):
    nombre = models.CharField(max_length=30, null=True)
    descripcion = models.TextField(max_length=100, null=True)
    receta = models.CharField(max_length=1, null=True)
    precio = models.FloatField(null=True)
    stock = models.IntegerField(null=True)


class Compra(models.Model):
    fecha = models.DateField(null=True)
    idPaciente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    precio = models.FloatField(null=True)


class Compra_medicamento(models.Model):
    idCompra = models.ForeignKey(Compra, on_delete=models.CASCADE, null=True)
    idMedicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, null=True)
    cant = models.IntegerField(null=True)
