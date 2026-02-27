from datetime import datetime

from django import forms

from appointments.models import Appointment
from users.models import User


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["idMedico"].queryset = User.objects.filter(is_medico=True)

    class Meta:
        model = Appointment
        fields = ["fecha", "idMedico"]
        labels = {"fecha": "Fecha", "idMedico": "Medico"}
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha < datetime.date(datetime.now()):
            raise forms.ValidationError("La fecha debe ser mayor o igual a la actual")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        medico = cleaned_data.get("idMedico")
        if fecha and medico and Appointment.objects.filter(fecha=fecha, idMedico=medico).count() > 3:
            raise forms.ValidationError("Ese medico no esta disponible en esa fecha")
        return cleaned_data


class AppointmentTreatmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["observaciones"]
        labels = {"observaciones": "Observaciones"}
        widgets = {
            "observaciones": forms.Textarea(attrs={"class": "form-control"}),
        }
