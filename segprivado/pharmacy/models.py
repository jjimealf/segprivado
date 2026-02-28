from django.conf import settings
from django.db import models


class Medicine(models.Model):
    nombre = models.CharField(max_length=30, null=True)
    descripcion = models.TextField(max_length=100, null=True)
    receta = models.CharField(max_length=1, null=True)
    precio = models.FloatField(null=True)
    stock = models.IntegerField(null=True)


class Purchase(models.Model):
    fecha = models.DateField(null=True)
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    precio = models.FloatField(null=True)


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    cant = models.IntegerField(null=True)
