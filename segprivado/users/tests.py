from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from pharmacy.models import Medicine


class AuthFlowTests(TestCase):
    def test_signup_creates_patient_user(self):
        response = self.client.post(
            reverse("registro"),
            {
                "username": "nuevo_paciente",
                "email": "nuevo@example.com",
                "password1": "ClaveSegura123",
                "password2": "ClaveSegura123",
            },
        )

        self.assertRedirects(response, "{}?register=1".format(reverse("login")))
        user = get_user_model().objects.get(username="nuevo_paciente")
        self.assertTrue(user.is_paciente)
        self.assertFalse(user.is_medico)

    def test_login_redirects_to_home(self):
        user = get_user_model().objects.create_user(
            username="paciente_login",
            password="ClaveSegura123",
            is_paciente=True,
            is_medico=False,
        )

        response = self.client.post(
            reverse("login"),
            {
                "username": user.username,
                "password": "ClaveSegura123",
            },
        )

        self.assertRedirects(response, reverse("home"))

    def test_seed_demo_is_idempotent(self):
        call_command("seed_demo")
        call_command("seed_demo")

        self.assertTrue(get_user_model().objects.filter(username="admin").exists())
        self.assertTrue(get_user_model().objects.filter(username="doctor_demo").exists())
        self.assertTrue(get_user_model().objects.filter(username="paciente_demo").exists())
        self.assertGreaterEqual(Medicine.objects.count(), 3)

    def test_logout_requires_post_and_ends_session(self):
        user = get_user_model().objects.create_user(
            username="paciente_logout",
            password="ClaveSegura123",
            is_paciente=True,
            is_medico=False,
        )
        self.client.force_login(user)

        get_response = self.client.get(reverse("logout"))
        self.assertEqual(get_response.status_code, 405)

        post_response = self.client.post(reverse("logout"))
        self.assertRedirects(post_response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
