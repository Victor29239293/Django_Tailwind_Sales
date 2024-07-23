from django.forms import ModelForm, TextInput, URLInput, EmailInput, FileInput, Select, CheckboxInput
from django import forms
from app.core.models import Company

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            "dni", "name", "address", "representative", "landline", "website",
            "email", "logo", "establishment_code", "emission_point_code",
            "authorization_number", "taxpayer_type", "required_to_keep_accounting",
            "economic_activity_code"
        ]
        widgets = {
            "dni": TextInput(
                attrs={
                    "placeholder": "Ingrese RUC",
                    "id": "id_dni",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "name": TextInput(
                attrs={
                    "placeholder": "Ingrese Nombre de la Empresa",
                    "id": "id_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "address": TextInput(
                attrs={
                    "placeholder": "Ingrese Dirección",
                    "id": "id_address",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "representative": TextInput(
                attrs={
                    "placeholder": "Ingrese Nombre del Responsable",
                    "id": "id_representative",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "landline": TextInput(
                attrs={
                    "placeholder": "Ingrese Teléfono Fijo",
                    "id": "id_landline",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "website": URLInput(
                attrs={
                    "placeholder": "Ingrese Sitio Web",
                    "id": "id_website",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "email": EmailInput(
                attrs={
                    "placeholder": "Ingrese Correo Electrónico",
                    "id": "id_email",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "logo": FileInput(
                attrs={
                    "type": "file",
                    "id": "id_logo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "establishment_code": TextInput(
                attrs={
                    "placeholder": "Ingrese Código de Establecimiento",
                    "id": "id_establishment_code",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "emission_point_code": TextInput(
                attrs={
                    "placeholder": "Ingrese Código de Punto de Emisión",
                    "id": "id_emission_point_code",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "authorization_number": TextInput(
                attrs={
                    "placeholder": "Ingrese Número de Autorización",
                    "id": "id_authorization_number",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "taxpayer_type": Select(
                attrs={
                    "id": "id_taxpayer_type",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "required_to_keep_accounting": CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "economic_activity_code": TextInput(
                attrs={
                    "placeholder": "Ingrese Código de Actividad Económica",
                    "id": "id_economic_activity_code",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "dni": "RUC",
            "name": "Empresa",
            "address": "Dirección",
            "representative": "Responsable",
            "landline": "Teléfono Fijo",
            "website": "Sitio Web",
            "email": "Correo Electrónico",
            "logo": "Logo",
            "establishment_code": "Código de Establecimiento",
            "emission_point_code": "Código de Punto de Emisión",
            "authorization_number": "Número de Autorización",
            "taxpayer_type": "Tipo de Contribuyente",
            "required_to_keep_accounting": "Obligado a Llevar Contabilidad",
            "economic_activity_code": "Código de Actividad Económica",
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        return name.upper()
