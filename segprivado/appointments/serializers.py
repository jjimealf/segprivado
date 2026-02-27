from rest_framework import serializers

from appointments.models import Appointment
from users.models import User


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "is_paciente", "is_medico", "is_active", "date_joined", "username"]


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "is_paciente", "is_medico", "is_active", "date_joined", "username"]


class AppointmentSerializer(serializers.ModelSerializer):
    idPaciente = PatientSerializer(read_only=True)
    idMedico = DoctorSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "idPaciente", "idMedico", "fecha", "observaciones"]
