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
    
# class SupplierUpdateView(PermissionMixin,UpdateViewMixin, UpdateView):
#     model = User
#     template_name = 'security/auth/form.html'
#     form_class = SupplierForm
#     success_url = reverse_lazy('core:supplier_list')
#     permission_required = 'change_supplier'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         context['grabar'] = 'Actualizar Proveedor'
#         context['back_url'] = self.success_url
#         return context
    
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         supplier = self.object
#         messages.success(self.request, f"Éxito al actualizar el proveedor {supplier.name}.")
#         return response
    
# class SupplierDeleteView(PermissionMixin,DeleteViewMixin, DeleteView):
#     model = Supplier
#     template_name = 'core/delete.html'
#     success_url = reverse_lazy('core:supplier_list')
#     permission_required = 'delete_supplier'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         context['grabar'] = 'Eliminar Proveedorl'
#         context['description'] = f"¿Desea Eliminar al Proveedor: {self.object.name}?"
#         context['back_url'] = self.success_url
#         return context
    
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         success_message = f"Éxito al eliminar lógicamente al proveedor {self.object.name}."
#         messages.success(self.request, success_message)
#         # Cambiar el estado de eliminado lógico
#         # self.object.deleted = True
#         # self.object.save()
#         return super().delete(request, *args, **kwargs)
    
