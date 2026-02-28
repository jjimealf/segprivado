from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from pharmacy.models import Medicine


class MedicineAdminFlowTests(TestCase):
    def test_staff_can_create_list_and_delete_medicine(self):
        staff_user = get_user_model().objects.create_user(
            username="staff_farmacia",
            password="ClaveSegura123",
            is_staff=True,
            is_superuser=True,
            is_paciente=False,
            is_medico=False,
        )
        self.client.force_login(staff_user)

        create_response = self.client.post(
            reverse("nucleo:crearMedicamento"),
            {
                "nombre": "Aspirina",
                "descripcion": "Analgesico",
                "receta": "N",
                "precio": "9.5",
                "stock": "12",
            },
        )

        self.assertRedirects(create_response, reverse("nucleo:indexMedicamento"))
        medicine = Medicine.objects.get(nombre="Aspirina")

        list_response = self.client.get(reverse("nucleo:indexMedicamento"))
        self.assertContains(list_response, "Aspirina")

        delete_response = self.client.get(reverse("nucleo:eliminarMedicamento", args=[medicine.pk]))
        self.assertRedirects(delete_response, reverse("nucleo:indexMedicamento"))
        self.assertFalse(Medicine.objects.filter(pk=medicine.pk).exists())
