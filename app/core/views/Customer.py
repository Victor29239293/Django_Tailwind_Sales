from django.urls import reverse_lazy
from app.core.forms.customer import CustomerForm
from app.core.models import Customer
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin,DetailViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,DetailView

from django.contrib import messages
from django.db.models import Q


class CustomerListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/Customer/list.html'
    model = Customer
    context_object_name = 'customer'
    permission_required = 'view_customer'
    
    paginate_by = 1
    
    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(dni__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:customer_create')
        
        
        return context

class CustomerCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Customer
    template_name = 'core/Customer/form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('core:customer_list')
    permission_required = 'add_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Cliente'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        cliente = self.object
        messages.success(self.request, f"Éxito al crear el cliente {cliente.first_name}.")
        return response

class CustomerUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Customer
    template_name = 'core/Customer/form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('core:customer_list')
    permission_required = 'change_Customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Cliente'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        cliente = self.object
        messages.success(self.request, f"Éxito al actualizar la marca {cliente.first_name}.")
        return response

class CustomerDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Customer
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:customer_list')
    permission_required = 'delete_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Marca'
        context['description'] = f"¿Desea eliminar la marca: {self.object.description}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar la marca {self.object.description}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
    
class CustomerDetailView(PermissionMixin, DetailViewMixin, DetailView):
    model = Customer
    template_name = 'core/Customer/view.html'
    context_object_name = 'customer'
    permission_required = 'view_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    