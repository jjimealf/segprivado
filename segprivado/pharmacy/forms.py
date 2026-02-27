from datetime import datetime

from django import forms

from pharmacy.models import Medicine, Purchase


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["nombre", "descripcion", "receta", "precio", "stock"]
        labels = {
            "nombre": "Nombre",
            "descripcion": "Descripcion",
            "receta": "Receta",
            "precio": "Precio",
            "stock": "Stock",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control"}),
            "receta": forms.TextInput(attrs={"class": "form-control"}),
            "precio": forms.NumberInput(attrs={"class": "form-control"}),
            "stock": forms.NumberInput(attrs={"class": "form-control"}),
        }


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["fecha", "precio"]
        labels = {"fecha": "Fecha", "precio": "Total"}
        widgets = {
            "fecha": forms.DateInput(
                attrs={
                    "disabled": True,
                    "value": datetime.date(datetime.now()),
                }
            ),
            "precio": forms.NumberInput(
                attrs={
                    "disabled": True,
                    "value": 0.0,
                }
            ),
        }
