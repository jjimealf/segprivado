from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Specialty(models.TextChoices):
        MEDICO_FAMILIA = "MF", "Medico de Familia"
        DIGESTIVO = "DG", "Digestivo"
        NEUROLOGO = "NE", "Neurologo"
        DERMATOLOGO = "DT", "Dermatologo"
        TRAUMATOLOGO = "TR", "Traumatologo"
        SIN_ESPECIALIDAD = "SE", "Sin Especialidad"

    edad = models.PositiveIntegerField(null=True, blank=True)
    especialidad = models.CharField(
        max_length=2,
        choices=Specialty.choices,
        default=Specialty.SIN_ESPECIALIDAD,
    )
    is_paciente = models.BooleanField("paciente status", default=True)
    is_medico = models.BooleanField("medico status", default=False)
    direccion = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to="users/photos/", null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_medico:
            self.is_paciente = False
        super().save(*args, **kwargs)

    def __str__(self):
        full_name = self.get_full_name().strip()
        return full_name or self.username
