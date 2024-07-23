from app.security.models import User
from django import forms
# from django.utils import timezone
# from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "Ingrese contraseña",
            "id": "id_password1",
            "class": "pl-10 shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "Confirmar contraseña",
            "id": "id_password2",
            "class": "pl-10 shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
        }
    ))

    class Meta:
        model = User
        fields = [
            'image',
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'dni', 
            'direction',
            'phone',
            # 'is_staff',
            # 'is_active',
            'password1',
            'password2',
            # 'is_superuser',
            # 'groups',
        ]
        labels = {
            "image": "Imagen",
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "dni": "DNI",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "direction": "Dirección",
            "phone": "Teléfono",
            # "is_staff": "Is staff",
            # "is_active": "Está activo",
            "password1": "Password",
            "password2": "Password confirmation",
            # "is_superuser": "Is Superuser",
            # "groups": "Grupos",
        }
        widgets = {
            "image": forms.FileInput(
                attrs={
                    "type": "file",
                    "id": "id_image",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese nombre de usuario",
                    "id": "id_username",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese nombre",
                    "id": "id_first_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese apellido",
                    "id": "id_last_name",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Ingrese correo electrónico",
                    "id": "id_email",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "dni": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese DNI",
                    "id": "id_dni",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "direction": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese dirección",
                    "id": "id_direction",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese teléfono",
                    "id": "id_phone",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            # "is_staff": forms.CheckboxInput(
            #     attrs={
            #         "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            #     }
            # ),
            # "is_active": forms.CheckboxInput(
            #     attrs={
            #         "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            #         'readonly': True,
            #     }
            # ),
            # "is_superuser": forms.CheckboxInput(
            #     attrs={
            #         "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            #         'readonly': True,
            #     }
            # ),
            # "groups": forms.CheckboxSelectMultiple(
            #     attrs={
            #         "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            #     }
            # ),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # self.save_m2m()
        return user


class CustomUserUpdateForm(forms.ModelForm):
        class Meta:
            model = User
            fields = [
                'image',
                'username', 
                'first_name', 
                'last_name', 
                'email', 
                'dni', 
                'direction',
                'phone',
                'is_active',
            ]
            
            labels = {
                "image": "Imagen",
                "username": "Nombre de usuario",
                "email": "Correo electrónico",
                "dni": "DNI",
                "first_name": "Nombre",
                "last_name": "Apellido",
                "direction": "Dirección",
                "phone": "Teléfono",
                "is_active": "Activo",
            }
            
            widgets = {
                "image": forms.FileInput(
                    attrs={
                        "type": "file",
                        "id": "id_image",
                        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    }
                ),
                "username": forms.TextInput(
                    attrs={
                        "placeholder": "Ingrese nombre de usuario",
                        "id": "id_username",
                        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    }
                ),
                "first_name": forms.TextInput(
                    attrs={
                        "placeholder": "Ingrese nombre",
                        "id": "id_first_name",
                        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    }
                ),
                "last_name": forms.TextInput(
                    attrs={
                        "placeholder": "Ingrese apellido",
                        "id": "id_last_name",
                        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    }
                ),
                "email": forms.EmailInput(
                    attrs={
                        "placeholder": "Ingrese correo electrónico",
                        "id": "id_email",
                        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    }
                ),
                "dni": forms.TextInput(
                    attrs={
                        "placeholder": "Ingrese DNI",
                        "id": "id_dni",
                        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    }
                ),
                "direction": forms.TextInput(
                    attrs={
                        "placeholder": "Ingrese dirección",
                        "id": "id_direction",
                        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    }
                ),
                "phone": forms.TextInput(
                    attrs={
                        "placeholder": "Ingrese teléfono",
                        "id": "id_phone",
                        "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                    }
                ),
                "is_active": forms.CheckboxInput(
                    attrs={
                        "class": "mt-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                    }
                ),
            }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Contraseña actual',
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña actual",
                'class': 'w-full pl-10 shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light'
            })
    )
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Nueva contraseña",
                'class': 'w-full pl-10 shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light'
            })
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmar nueva contraseña",
                'class': 'w-full pl-10 shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light'
            })
    )

    class Meta:
        model = User
        fields = [
            'old_password', 
            'new_password1', 
            'new_password2'
        ]

        