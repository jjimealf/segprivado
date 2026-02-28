from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from pharmacy.models import Medicine


class Command(BaseCommand):
    help = "Create minimal demo data for a fresh local database."

    def handle(self, *args, **options):
        user_model = get_user_model()

        admin_user, admin_created = user_model.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
                "is_medico": False,
                "is_paciente": False,
            },
        )
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_medico = False
        admin_user.is_paciente = False
        admin_user.set_password("admin12345")
        admin_user.save()

        doctor, doctor_created = user_model.objects.get_or_create(
            username="doctor_demo",
            defaults={
                "email": "doctor@example.com",
                "first_name": "Demo",
                "last_name": "Doctor",
                "is_medico": True,
                "is_paciente": False,
                "especialidad": user_model.Specialty.MEDICO_FAMILIA,
            },
        )
        doctor.is_medico = True
        doctor.is_paciente = False
        doctor.set_password("doctor12345")
        doctor.save()

        patient, patient_created = user_model.objects.get_or_create(
            username="paciente_demo",
            defaults={
                "email": "paciente@example.com",
                "first_name": "Demo",
                "last_name": "Paciente",
                "is_medico": False,
                "is_paciente": True,
            },
        )
        patient.is_medico = False
        patient.is_paciente = True
        patient.set_password("paciente12345")
        patient.save()

        sample_medicines = [
            ("Paracetamol", "Analgesico basico", "N", 5.5, 30),
            ("Ibuprofeno", "Antiinflamatorio", "N", 7.0, 20),
            ("Amoxicilina", "Antibiotico", "S", 12.5, 15),
        ]

        medicines_created = 0
        for nombre, descripcion, receta, precio, stock in sample_medicines:
            _, created = Medicine.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": descripcion,
                    "receta": receta,
                    "precio": precio,
                    "stock": stock,
                },
            )
            if created:
                medicines_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Seed completado: admin({}), doctor({}), paciente({}), medicamentos nuevos({})".format(
                    "creado" if admin_created else "actualizado",
                    "creado" if doctor_created else "actualizado",
                    "creado" if patient_created else "actualizado",
                    medicines_created,
                )
            )
        )
