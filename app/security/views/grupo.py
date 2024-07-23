from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q
from app.security.models import GroupModulePermission, Module, Permission, Group
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from app.security.forms.grupos_modulos_permi import GroupModulePermissionForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from app.security.mixins.mixins import CreateViewMixin, ListViewMixin, UpdateViewMixin, DeleteViewMixin

class GroupModulePermissionListView(ListViewMixin, ListView):
    template_name = 'security/GroupModulePermission/list.html'
    model = GroupModulePermission
    context_object_name = "group_module_permissions"
    permission_required = "security.view_groupmodulepermission"
    paginate_by = 5
    
    def get_queryset(self):
        queryset = super().get_queryset()
        q1 = self.request.GET.get('q')
        if q1:
            queryset = queryset.filter(Q(group__name__icontains=q1))
        return queryset.order_by("id")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permission_add'] = self.request.user.has_perm('security.add_groupmodulepermission')
        context['create_url'] = reverse_lazy('security:group_module_permission_create')
        return context

class GroupModulePermissionCreateView(CreateViewMixin, CreateView):
    model = GroupModulePermission
    template_name = "security/GroupModulePermission/form.html"
    form_class = GroupModulePermissionForm
    permission_required = "security.add_groupmodulepermission"
    success_url = reverse_lazy('security:group_module_permission_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar grupo modulo permiso'
        context['back_url'] = self.success_url
        context['groups'] = Group.objects.all()  # Obtener todos los grupos para la plantilla
        return context
    
    def post(self, request, *args, **kwargs):
        if 'module_id' in request.POST:
            module_id = request.POST['module_id']
            module = get_object_or_404(Module, id=module_id)
            content_type = ContentType.objects.get(app_label=module.url)
            permissions = Permission.objects.filter(content_type=content_type)
            data = [{"id": perm.id, "name": perm.name} for perm in permissions]
            return JsonResponse(data, safe=False)
        return super().post(request, *args, **kwargs)
    
    
class GroupModulePermissionUpdateView(UpdateViewMixin, UpdateView):
    model = GroupModulePermission
    template_name = "security/GroupModulePermission/form.html"
    form_class = GroupModulePermissionForm
    permission_required = "security.change_groupmodulepermission"
    success_url = reverse_lazy('security:group_module_permission_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar grupo modulo permiso'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        groupmodule = self.object
        messages.success(self.request, f"Éxito al actualizar el Módulo {groupmodule.module.name}.")
        return response

    def post(self, request, *args, **kwargs):
        if 'module_id' in request.POST:
            module_id = request.POST['module_id']
            module = get_object_or_404(Module, id=module_id)
            permissions = module.permissions.all()  # Obtener solo los permisos del módulo seleccionado
            data = [{"id": perm.id, "name": perm.name} for perm in permissions]
            return JsonResponse(data, safe=False)
        return super().post(request, *args, **kwargs)

class GroupModulePermissionDeleteView(DeleteViewMixin, DeleteView):
    model = GroupModulePermission
    template_name = "security/GroupModulePermission/delete.html"
    success_url = reverse_lazy('security:group_module_permission_list')
    permission_required = "security.delete_groupmodulepermission"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        module_name = self.object.module.name
        self.object.delete()
        messages.success(request, f"El grupo módulo permiso {module_name} ha sido eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = self.success_url
        return context

def get_module_permissions(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    permissions = module.permissions.all()  # Asegúrate de que esto esté filtrando los permisos correctamente
    permissions_data = [{'id': perm.id, 'name': perm.name} for perm in permissions]
    return JsonResponse(permissions_data, safe=False)


