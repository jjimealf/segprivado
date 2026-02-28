from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["password"].label = "Contrasena"
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Usuario", "autocomplete": "username"}
        )
        self.fields["password"].widget.attrs.update(
            {"placeholder": "Contrasena", "autocomplete": "current-password"}
        )


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Usuario"
        self.fields["email"].label = "Correo"
        self.fields["password1"].label = "Contrasena"
        self.fields["password2"].label = "Repetir contrasena"
        self.fields["username"].help_text = ""
        self.fields["email"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Usuario", "autocomplete": "username"}
        )
        self.fields["email"].widget.attrs.update(
            {"placeholder": "Correo", "autocomplete": "email"}
        )
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Contrasena", "autocomplete": "new-password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Repetir contrasena", "autocomplete": "new-password"}
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
        fields = ["username", "first_name", "last_name", "email", "direccion", "foto"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_config = {
            "username": ("Usuario", "Usuario"),
            "first_name": ("Nombre", "Nombre"),
            "last_name": ("Apellidos", "Apellidos"),
            "email": ("Correo", "Correo"),
            "direccion": ("Direccion", "Direccion"),
            "foto": ("Foto", None),
        }
        for name, (label, placeholder) in field_config.items():
            field = self.fields[name]
            field.label = label
            if placeholder:
                field.widget.attrs.update({"placeholder": placeholder})
        self.fields["email"].widget.attrs["autocomplete"] = "email"
        self.fields["foto"].widget.attrs["accept"] = "image/*"
