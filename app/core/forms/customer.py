from django.forms import ModelForm
from django import forms
from app.core.models import Customer

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = [
            "dni", "first_name", "last_name", "address", "gender", "date_of_birth",
            "phone", "email", "latitude", "longitude", "active", "image"
        ]
        error_messages = {
            "dni": {
                "unique": "Ya existe un proveedor con este RUC o DNI.",
            }
        }
        widgets = {
            "dni": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese Dni Cliente",
                    "id": "id_dni",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese Nombre del Cliente",
                    "id": "id_first_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese apellido del Cliente",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese Dirección",
                    "id": "id_address",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "gender": forms.Select(
                attrs={
                    "id": "id_gender",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "date_of_birth": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese Fecha de Nacimiento",
                    "id": "id_date_of_birth",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    "type": "date"
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese número celular",
                    "id": "id_phone",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Ingrese Correo Electrónico",
                    "id": "id_email",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "latitude": forms.TextInput(
                attrs={
                    "placeholder": "Coordenada: latitud",
                    "id": "id_latitude",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "longitude": forms.TextInput(
                attrs={
                    "placeholder": "Coordenada: longitud",
                    "id": "id_longitude",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "type": "file",
                    "id": "id_image",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            # Añade widgets para los campos adicionales aquí, si es necesario
        }
        labels = {
            "dni": "Dni",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "address": "Dirección",
            "gender": "Género",
            "date_of_birth": "Fecha de Nacimiento",
            "phone": "Celular",
            "email": "Correo Electrónico",
            "latitude": "Latitud",
            "longitude": "Longitud",
            "active": "Estado",
            "image": "Imagen",
        }

    def clean_name(self):
        name = self.cleaned_data.get("first_name")
        return name.upper()
