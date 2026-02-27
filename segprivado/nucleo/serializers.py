from rest_framework import serializers
from nucleo.models import Usuario, Cita 

class pacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'first_name', 'last_name', 'is_paciente', 'is_medico', 'is_active', 'date_joined', 'username']
        
class medicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'first_name', 'last_name', 'is_paciente', 'is_medico', 'is_active', 'date_joined', 'username']

class citaSerializer(serializers.ModelSerializer):
    idPaciente = pacienteSerializer(read_only=True)
    idMedico = medicoSerializer(read_only=True)
    class Meta:
        model = Cita
        fields = ['id', 'idPaciente', 'idMedico', 'fecha', 'observaciones']