from django.urls import reverse_lazy
from app.core.forms.payment_method import PaymentMethodForm
from app.core.models import PaymentMethod
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages

class PaymentMethodListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/payment_method/list.html'
    model = PaymentMethod
    context_object_name = 'payment_methods'
    permission_required = 'view_paymentmethod'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:paymentmethod_create')
        return context

class PaymentMethodCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = PaymentMethod
    template_name = 'core/payment_method/form.html'
    form_class = PaymentMethodForm
    success_url = reverse_lazy('core:payment_method_list')
    permission_required = 'add_paymentmethod'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Método de Pago'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        payment_method = self.object
        messages.success(self.request, f"Éxito al crear el método de pago {payment_method.description}.")
        return response

class PaymentMethodUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = PaymentMethod
    template_name = 'core/payment_method/form.html'
    form_class = PaymentMethodForm
    success_url = reverse_lazy('core:payment_method_list')
    permission_required = 'change_paymentmethod'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Método de Pago'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        payment_method = self.object
        messages.success(self.request, f"Éxito al actualizar el método de pago {payment_method.description}.")
        return response

class PaymentMethodDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = PaymentMethod
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:payment_method_list')
    permission_required = 'delete_paymentmethod'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Método de Pago'
        context['description'] = f"¿Desea eliminar el método de pago: {self.object.description}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el método de pago {self.object.description}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
