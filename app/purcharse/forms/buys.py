from django import forms
from app.purcharse.models import Purchase
from app.core.models import Supplier  # Asegúrate de importar el modelo Supplier

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["num_document", "supplier", "issue_date", "subtotal", "iva", "total", "active"]
        widgets = {
            "num_document": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese número de documento",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "supplier": forms.Select(
                attrs={
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "issue_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "readonly": "readonly",
                },
                format='%Y-%m-%dT%H:%M'
            ),
            "subtotal": forms.NumberInput(
                attrs={
                    "placeholder": "Ingrese subtotal",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "readonly": "readonly",
                }
            ),
            "iva": forms.NumberInput(
                attrs={
                    "placeholder": "Ingrese IVA",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "readonly": "readonly",
                }
            ),
            "total": forms.NumberInput(
                attrs={
                    "placeholder": "Ingrese total",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "readonly": "readonly",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "class": "shadow-sm bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "num_document": "Número de Documento",
            "supplier": "Proveedor",
            "issue_date": "Fecha de Emisión",
            "subtotal": "Subtotal",
            "iva": "IVA",
            "total": "Total",
            "active": "Activo",
        }
