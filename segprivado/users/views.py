from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import SignupForm, UserProfileForm


class Login(LoginView):
    template_name = "users/login.html"


class LogoutView(DjangoLogoutView):
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
