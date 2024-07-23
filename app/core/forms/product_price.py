from django.forms import ModelForm
from django import forms
from app.core.models import ProductPrice

class ProductPriceForm(ModelForm):
    class Meta:
        model = ProductPrice
        fields = [
            "line", "category", "product", "type_increment", "value", 
            "issue_date", "observaciones", "active"
        ]
        widgets = {
            "line": forms.Select(
                attrs={
                    "id": "id_line",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "category": forms.SelectMultiple(
                attrs={
                    "id": "id_category",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "product": forms.Select(
                attrs={
                    "id": "id_product",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "type_increment": forms.Select(
                attrs={
                    "id": "id_type_increment",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "value": forms.NumberInput(
                attrs={
                    "placeholder": "Ingrese el valor",
                    "id": "id_value",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "issue_date": forms.DateInput(
                attrs={
                    "placeholder": "Ingrese la fecha de emisión",
                    "id": "id_issue_date",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "type": "date"
                }
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "placeholder": "Ingrese observaciones",
                    "id": "id_observaciones",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
        }
        labels = {
            "line": "Linea",
            "category": "Categoría",
            "product": "Producto Precio",
            "type_increment": "Tipo de Aumento",
            "value": "Incremento",
            "issue_date": "Fecha Emisión",
            "observaciones": "Observaciones",
            "active": "Activo",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['issue_date'].initial = self.instance.issue_date

    def clean_observaciones(self):
        observaciones = self.cleaned_data.get("observaciones")
        return observaciones.strip() if observaciones else observaciones
