from django.urls import reverse_lazy
from app.core.forms.categoria import CategoriaForm
from app.core.models import Category
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

class CategoriaListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/categories/list.html'
    model = Category
    context_object_name = 'categories'
    permission_required = 'view_category'
    paginate_by = 5
    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(description__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:category_create')
        context['title1'] = 'Categorías'
        context['title2'] = 'Lista de Categorías'
        return context


class CategoriaCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Category
    template_name = 'core/categories/form.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('core:category_list')
    permission_required = 'add_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Categoría'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        categoria = self.object
        messages.success(self.request, f"Éxito al crear la Categoría {categoria.description}.")
        return response


class CategoriaUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Category
    template_name = 'core/categories/form.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('core:category_list')
    permission_required = 'change_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Categoría'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        categoria = self.object
        messages.success(self.request, f"Éxito al actualizar la Categoría {categoria.description}.")
        return response


class CategoriaDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Category
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:category_list')
    permission_required = 'delete_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Categoría'
        context['description'] = f"¿Desea eliminar la categoría: {self.object.description}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar la categoría {self.object.description}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
