from datetime import datetime

from django import forms

from appointments.models import Appointment
from users.models import User


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop("patient", None)
        super().__init__(*args, **kwargs)
        self.fields["doctor"].queryset = User.objects.filter(is_medico=True)
        self.fields["doctor"].empty_label = "Seleccionar"
        self.fields["fecha"].input_formats = ["%Y-%m-%d", "%d/%m/%Y", "%d/%m/%y"]
        self.fields["fecha"].widget.attrs.update(
            {
                "autocomplete": "off",
                "placeholder": "AAAA-MM-DD",
                "data-min-date": datetime.date(datetime.now()).isoformat(),
            }
        )
        self.fields["doctor"].widget.attrs.update({"autocomplete": "off"})

    class Meta:
        model = Appointment
        fields = ["fecha", "doctor"]
        labels = {"fecha": "Fecha", "doctor": "Medico"}
        widgets = {
            "fecha": forms.DateInput(format="%Y-%m-%d", attrs={"type": "text"}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data["fecha"]
        if fecha < datetime.date(datetime.now()):
            raise forms.ValidationError("La fecha debe ser mayor o igual a la actual")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        doctor = cleaned_data.get("doctor")
        if fecha and self.patient and Appointment.objects.filter(fecha=fecha, patient=self.patient).exists():
            raise forms.ValidationError("Ya tienes una cita registrada para esa fecha")
        if fecha and doctor and Appointment.objects.filter(fecha=fecha, doctor=doctor).count() > 3:
            raise forms.ValidationError("Ese medico no esta disponible en esa fecha")
        return cleaned_data


class AppointmentTreatmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["observaciones"]
        labels = {"observaciones": "Notas"}
        widgets = {
            "observaciones": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Notas",
                }
            ),
        }
