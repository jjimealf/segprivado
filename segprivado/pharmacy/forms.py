from datetime import datetime

from django import forms

from pharmacy.models import Medicine, Purchase


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["nombre", "descripcion", "receta", "precio", "stock"]
        labels = {
            "nombre": "Nombre",
            "descripcion": "Detalle",
            "receta": "Receta",
            "precio": "Precio",
            "stock": "Stock",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Nombre"}),
            "descripcion": forms.Textarea(attrs={"rows": 4, "placeholder": "Detalle"}),
            "receta": forms.TextInput(attrs={"placeholder": "Receta"}),
            "precio": forms.NumberInput(attrs={"placeholder": "Precio", "step": "0.01"}),
            "stock": forms.NumberInput(attrs={"placeholder": "Stock"}),
        }


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["fecha", "precio"]
        labels = {"fecha": "Fecha", "precio": "Total"}
        widgets = {
            "fecha": forms.DateInput(
                attrs={
                    "type": "date",
                    "disabled": True,
                    "value": datetime.date(datetime.now()),
                }
            ),
            "precio": forms.NumberInput(
                attrs={
                    "disabled": True,
                    "value": 0.0,
                    "step": "0.01",
                }
            ),
        }
