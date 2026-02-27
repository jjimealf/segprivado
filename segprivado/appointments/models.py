from django.conf import settings
from django.db import models


class Appointment(models.Model):
    fecha = models.DateField(null=True)
    observaciones = models.TextField(max_length=200, null=True)
    idMedico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="appointments_as_doctor",
    )
    idPaciente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="appointments_as_patient",
    )

    class Meta:
        ordering = ("fecha",)

    @property
    def doctor(self):
        return self.idMedico

    @property
    def patient(self):
        return self.idPaciente
