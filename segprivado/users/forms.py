from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Nombre de usuario"}
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Correo"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Contrasena"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Repite la contrasena"}
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_paciente = True
        user.is_medico = False
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "direccion"]
