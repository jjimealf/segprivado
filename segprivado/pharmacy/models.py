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
    idPaciente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    precio = models.FloatField(null=True)

    @property
    def patient(self):
        return self.idPaciente


class PurchaseItem(models.Model):
    idCompra = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    idMedicamento = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True)
    cant = models.IntegerField(null=True)

    @property
    def purchase(self):
        return self.idCompra

    @property
    def medicine(self):
        return self.idMedicamento
