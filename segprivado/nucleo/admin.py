from django import forms
from django.contrib import admin

from .models import Cita, Medicamento

class MedicamentoAdminForm(forms.ModelForm):
   def clean_receta(self):
      receta = self.cleaned_data['receta']
      if receta != 'S' and receta != 'N':
         raise forms.ValidationError("Debe ser S o N")
      else:
         return receta

class MedicamentoAdmin(admin.ModelAdmin):
   form = MedicamentoAdminForm
   search_fields = ['nombre']
         
# Register your models here.
admin.site.register(Medicamento, MedicamentoAdmin)
admin.site.register(Cita)
