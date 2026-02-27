from django import forms
from django.contrib.auth.forms import UserCreationForm
from nucleo.models import Usuario
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class UserCreationFormEmail(UserCreationForm):
    email=forms.EmailField(required=True, help_text="Requerido")

    class Meta:
        model=Usuario
        fields=('username','password1','password2','email')

    def save(self,comit=True):
        user=super(UserCreationFormEmail, self).save()
        user.email = self.cleaned_data["email"]
        user.save()
        return user

class EditUserProfileForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields=['username','first_name', 'last_name', 'direccion']