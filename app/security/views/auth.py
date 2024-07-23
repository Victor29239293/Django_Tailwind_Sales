from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from app.security.forms.user import CustomUserCreationForm, CustomUserUpdateForm, CustomPasswordChangeForm
from app.security.models import User
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


# ----------------- Perfil -----------------
def profile(request, pk=id):
    data = {"title1": "IC - Perfil",
            "title2": "Perfil de Usuario"}
    return render(request, 'core/profile.html', data)

# ----------------- Cambiar password -----------------
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'core/password_change_form.html'

    def get_success_url(self):
        return reverse_lazy('security:auth_profile', kwargs={'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'IC - Change password'
        context['title2'] = 'Change password'
        context['back_url'] = reverse_lazy('security:auth_profile', kwargs={'pk': self.request.user.pk})
        return context

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, '¡Tu contraseña ha sido actualizada exitosamente!')
        return super().form_valid(form)

# ----------------- Actualizar perfil -----------------
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'core/update_profile.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse_lazy('security:auth_profile', kwargs={'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'IC - Actualizar Perfil'
        context['title2'] = 'Actualizar Perfil'
        context['back_url'] = reverse_lazy('security:auth_profile', kwargs={'pk': self.request.user.pk})
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Tu perfil ha sido actualizado exitosamente!')
        return response

# ----------------- Registro -----------------
def signup(request):
    data = {"title1": "IC - Registro",
            "title2": "Registro de Usuarios"}

    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "security/auth/signup.html", {"form": form, **data})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # groups = form.cleaned_data['groups']
            # user.groups.set(groups)
            # user.save()
            # login(request, user)
            messages.success(
                request, '¡Registro exitoso! Por favor, inicia sesión.')
            return redirect("security:auth_login")
        else:
            # Manejo de errores específicos
            if form.errors:
                error_messages = []
                for field in form:
                    for error in field.errors:
                        error_messages.append(f"{field.label}: {error}")
                for error in form.non_field_errors():
                    error_messages.append(error)
                data["errors"] = error_messages

            return render(request, "security/auth/signup.html", {"form": form, **data})

# # ----------------- Cerrar Sesion -----------------
@login_required
def signout(request):
    logout(request)
    return redirect("home")

# # ----------------- Iniciar Sesion -----------------
def signin(request):
    
    data = {"title1": "IC - Login",
            "title2": "Inicio de Sesión"}
    if request.method == "GET":
        # Obtener mensajes de éxito de la cola de mensajes
        success_messages = messages.get_messages(request)
        return render(request, "security/auth/signin.html", {
            "form": AuthenticationForm(),
            "success_messages": success_messages,  # Pasar mensajes de éxito a la plantilla
            **data
        })
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("modulos")
            else:
                return render(request, "security/auth/signin.html", {
                    "form": form,
                    "error": "El usuario o la contraseña son incorrectos",
                    **data
                })
        else:
            return render(request, "security/auth/signin.html", {
                "form": form,
                 "error": "Datos invalidos",
                **data
            })
