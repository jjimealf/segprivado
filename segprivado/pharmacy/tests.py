from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from pharmacy.models import Medicine, Purchase, PurchaseItem


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


class PurchaseFlowTests(TestCase):
    def test_patient_can_confirm_purchase_and_stock_is_discounted(self):
        patient = get_user_model().objects.create_user(
            username="paciente_farmacia",
            password="ClaveSegura123",
            is_paciente=True,
            is_medico=False,
            is_staff=False,
        )
        medicine = Medicine.objects.create(
            nombre="Ibuprofeno",
            descripcion="Antiinflamatorio",
            receta="N",
            precio=7.5,
            stock=4,
        )

        self.client.force_login(patient)
        self.client.get(reverse("nucleo:addMedicamento", args=[medicine.pk]))
        self.client.get(reverse("nucleo:addMedicamento", args=[medicine.pk]))

        response = self.client.post(reverse("nucleo:pedirCompra"))

        self.assertRedirects(response, reverse("nucleo:pedirCompra"))
        purchase = Purchase.objects.get()
        purchase_item = PurchaseItem.objects.get()
        medicine.refresh_from_db()

        self.assertEqual(purchase.patient, patient)
        self.assertEqual(purchase.precio, 15.0)
        self.assertEqual(purchase_item.purchase, purchase)
        self.assertEqual(purchase_item.medicine, medicine)
        self.assertEqual(purchase_item.cant, 2)
        self.assertEqual(medicine.stock, 2)
        self.assertEqual(self.client.session.get("carrito"), {})

    def test_purchase_is_rejected_if_requested_quantity_exceeds_stock(self):
        patient = get_user_model().objects.create_user(
            username="paciente_farmacia_stock",
            password="ClaveSegura123",
            is_paciente=True,
            is_medico=False,
            is_staff=False,
        )
        medicine = Medicine.objects.create(
            nombre="Paracetamol",
            descripcion="Analgesico",
            receta="N",
            precio=5.0,
            stock=1,
        )

        self.client.force_login(patient)
        session = self.client.session
        session["carrito"] = {
            str(medicine.pk): {
                "id": medicine.pk,
                "nombre": medicine.nombre,
                "descripcion": medicine.descripcion,
                "precio": medicine.precio,
                "acumulado": 10.0,
                "cantidad": 2,
            }
        }
        session.save()
        response = self.client.post(reverse("nucleo:pedirCompra"))

        self.assertRedirects(response, reverse("nucleo:pedirCompra"))
        medicine.refresh_from_db()
        self.assertFalse(Purchase.objects.exists())
        self.assertFalse(PurchaseItem.objects.exists())
        self.assertEqual(medicine.stock, 1)
        self.assertIn(str(medicine.pk), self.client.session.get("carrito", {}))

    def test_patient_can_view_only_their_purchase_history(self):
        patient = get_user_model().objects.create_user(
            username="paciente_historial",
            password="ClaveSegura123",
            is_paciente=True,
            is_medico=False,
            is_staff=False,
        )
        other_patient = get_user_model().objects.create_user(
            username="paciente_historial_otro",
            password="ClaveSegura123",
            is_paciente=True,
            is_medico=False,
            is_staff=False,
        )
        medicine = Medicine.objects.create(
            nombre="Omeprazol",
            descripcion="Protector gastrico",
            receta="N",
            precio=6.0,
            stock=5,
        )
        other_medicine = Medicine.objects.create(
            nombre="Vitamina C",
            descripcion="Suplemento",
            receta="N",
            precio=4.0,
            stock=5,
        )
        purchase = Purchase.objects.create(patient=patient, precio=12.0)
        other_purchase = Purchase.objects.create(patient=other_patient, precio=4.0)
        PurchaseItem.objects.create(purchase=purchase, medicine=medicine, cant=2)
        PurchaseItem.objects.create(purchase=other_purchase, medicine=other_medicine, cant=1)

        self.client.force_login(patient)
        response = self.client.get(reverse("nucleo:historialCompra"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Omeprazol")
        self.assertContains(response, "Compra #{}".format(purchase.pk))
        self.assertNotContains(response, "Vitamina C")
        self.assertNotContains(response, "Compra #{}".format(other_purchase.pk))
