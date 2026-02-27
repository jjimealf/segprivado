
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    MedicodeFamilia= 'MF'
    Digestivo= 'DG'
    Neurologo= 'NE'
    Dermatologo= 'DT'
    Traumatologo= 'TR'
    SinEspecialidad= 'SE'
    ESPECIALIDAD_CHOICES = [(MedicodeFamilia, 'Medico de Familia'),(Digestivo, 'Digestivo'),(Neurologo, 'Neurologo'),(Dermatologo, 'Dermatologo'),(Traumatologo, 'Traumatologo'),(SinEspecialidad, 'Sin Especialidad')]
    first_name = models.CharField(max_length=30, verbose_name="Nombre", null=True)
    last_name = models.CharField(max_length=30, verbose_name="Apellidos", null=True)
    edad = models.IntegerField(null=True)
    date_joined = models.DateTimeField(verbose_name="Fecha de alta", null=True)
    especialidad = models.CharField(max_length=2, choices=ESPECIALIDAD_CHOICES, default=SinEspecialidad)
    username = models.CharField(max_length=30, unique=True, verbose_name="Usuario", null=True)
    password = models.CharField(max_length=100, verbose_name="Contraseña", null=True)
    is_active = models.BooleanField(verbose_name="Activo", default=False)
    is_paciente = models.BooleanField('paciente status',null=True)
    is_medico = models.BooleanField('medico status',null=True)
    direccion = models.CharField(max_length=100, null=True)
    foto = models.ImageField(upload_to='fotos/', null=True)

    def __str__(self):
        if self.first_name is not None or self.last_name is not None:
            return self.first_name + " " + self.last_name
        return self.username
    
    
class Cita(models.Model):
    fecha = models.DateField(null=True)
    observaciones = models.TextField(max_length=200, null=True)
    idMedico = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, related_name='medico')
    idPaciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, related_name='paciente')
    
    class Meta:
        ordering = ('fecha',)

class Medicamento(models.Model):
    nombre = models.CharField(max_length=30, null=True)
    descripcion = models.TextField(max_length=100, null=True)
    receta = models.CharField(max_length=1, null=True)
    precio = models.FloatField(null=True)
    stock = models.IntegerField(null=True)
    
class Compra(models.Model):
    fecha = models.DateField(null=True)
    idPaciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)
    precio = models.FloatField(null=True)
    
class Compra_medicamento(models.Model):
    idCompra = models.ForeignKey(Compra, on_delete=models.CASCADE, null=True)
    idMedicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, null=True)
    cant = models.IntegerField(null=True)