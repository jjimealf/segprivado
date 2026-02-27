from django.shortcuts import render
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from registration.forms import EditUserProfileForm, UserCreationFormEmail
from nucleo.models import Usuario

# Create your views here.

class Login(LoginView):
    template_name = 'registration/login.html'


class SignupView(CreateView):
    form_class=UserCreationFormEmail
    template_name='registration/register.html'

    def get_succes_url(self):
        return reverse_lazy('login')+'?register'

    def get_form(self, form_class=None):
        form=super(SignupView,self).get_form()
        form.fields['username'].widget=forms.TextInput(attrs={'class':'form-control mb2',
        'placeholder':'Nombre de usuario'})
        form.fields['email'].widget=forms.EmailInput(attrs={'class':'form-control mb2',
        'placeholder':'Mail'})
        form.fields['password1'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
        'placeholder':'Contraseña'})
        form.fields['password2'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
        'placeholder':'Repite la contraseña'})
        return form

class UserEditView(UpdateView):
    form_class = EditUserProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('nucleo:home')

    def get_object(self):
        return self.request.user

class medicosEspecilidad(ListView):
   model = Usuario
   template_name = 'especialidad.html'

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      especialidadGet = self.request.GET.get('especialidad')
      
      if(self.request.GET.get('especialidad')!=0):
         data = Usuario.objects.filter(especialidad=especialidadGet, is_medico=True)
      else:
         data = Usuario.objects.all()
      
      context['data'] = data
      return context