from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from appointments.models import Appointment


class AppointmentFlowTests(TestCase):
    def test_patient_can_create_appointment(self):
        user_model = get_user_model()
        patient = user_model.objects.create_user(
            username="paciente_cita",
            password="ClaveSegura123",
            is_paciente=True,
            is_medico=False,
        )
        doctor = user_model.objects.create_user(
            username="doctor_cita",
            password="ClaveSegura123",
            is_paciente=False,
            is_medico=True,
        )

        self.client.force_login(patient)
        response = self.client.post(
            reverse("nucleo:pedirCita"),
            {
                "fecha": (date.today() + timedelta(days=1)).isoformat(),
                "doctor": doctor.pk,
            },
        )

        self.assertRedirects(response, reverse("nucleo:home"))
        appointment = Appointment.objects.get()
        self.assertEqual(appointment.patient, patient)
        self.assertEqual(appointment.doctor, doctor)
