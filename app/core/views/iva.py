from django.urls import reverse_lazy
from app.core.forms.iva import IvaForm
from app.core.models import Iva
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages

class IvaListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/iva/list.html'
    model = Iva
    context_object_name = 'ivas'
    permission_required = 'view_iva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:iva_create')
        return context

class IvaCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Iva
    template_name = 'core/iva/form.html'
    form_class = IvaForm
    success_url = reverse_lazy('core:iva_list')
    permission_required = 'add_iva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Iva'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        iva = self.object
        messages.success(self.request, f"Éxito al crear el Iva {iva.description}.")
        return response

class IvaUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Iva
    template_name = 'core/iva/form.html'
    form_class = IvaForm
    success_url = reverse_lazy('core:iva_list')
    permission_required = 'change_iva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Iva'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        iva = self.object
        messages.success(self.request, f"Éxito al actualizar el Iva {iva.description}.")
        return response

class IvaDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Iva
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:iva_list')
    permission_required = 'delete_iva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Iva'
        context['description'] = f"¿Desea eliminar el Iva: {self.object.description}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el Iva {self.object.description}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
