from django.urls import reverse_lazy
from app.security.forms.user import UserForm
from app.security.models import User
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
# from django.db.models import Q


class UserCreateView(PermissionMixin,CreateViewMixin, CreateView):
    model = User
    template_name = 'security/auth/signup.html'
    form_class = UserForm
    success_url = reverse_lazy('core:modulos')
    permission_required = 'add_user' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar User'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        messages.success(self.request, f"Éxito al crear al User {user.first_name}.")
        return response
    