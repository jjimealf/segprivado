from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.views import LoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import CreateView, UpdateView

from users.forms import LoginForm, SignupForm, UserProfileForm


class Login(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm


class LogoutView(DjangoLogoutView):
    http_method_names = ["post", "options"]
    next_page = reverse_lazy("login")


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "users/register.html"

    def get_success_url(self):
        return "{}?register=1".format(reverse_lazy("login"))


class UserEditView(UpdateView):
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("nucleo:home")

    def get_object(self, queryset=None):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.all()


class ApiLoginView(APIView):
    def get(self, request, format=None):
        return Response({"detail": "GET Response"})

    def post(self, request, format=None):
        username = request.data.get("user")
        password = request.data.get("password")
        if not username or not password:
            return Response({"detail": "Credenciales incorrectas"}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"detail": "Credenciales incorrectas"}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_paciente or not user.is_active:
            return Response({"detail": "Usuario no autorizado"}, status=status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
