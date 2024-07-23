from django.urls import reverse_lazy
from app.core.forms.product_price import ProductPriceForm
from app.core.models import ProductPrice, ProductPriceDetail
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q


class ProductPriceListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/product_price/list.html'
    model = ProductPrice
    context_object_name = 'product_prices'
    permission_required = 'view_productprice'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:productprice_list')
        return context
    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(description__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).order_by('id')

class ProductPriceCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = ProductPrice
    template_name = 'core/product_price/form.html'
    form_class = ProductPriceForm
    success_url = reverse_lazy('core:productprice_list')
    permission_required = 'add_productprice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Precio del Producto'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        product_price = self.object
        self.update_product_prices(product_price)
        messages.success(self.request, f"Éxito al crear el precio del producto {product_price.product.description}.")
        return response

    def update_product_prices(self, product_price):
        for detail in product_price.productPrice_detail.all():
            product = detail.product
            new_price = detail.new_price
            product.price = new_price
            product.save()
            print(f"Updated {product.description} to new price {new_price}")  # Debugging statement


class ProductPriceUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = ProductPrice
    template_name = 'core/product_price/form.html'
    form_class = ProductPriceForm
    success_url = reverse_lazy('core:productprice_list')
    permission_required = 'change_productprice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Precio del Producto'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        product_price = self.object
        self.update_product_prices(product_price)
        messages.success(self.request, f"Éxito al actualizar el precio del producto {product_price.product.description}.")
        return response

    def update_product_prices(self, product_price):
        for detail in product_price.productPrice_detail.all():
            product = detail.product
            new_price = detail.new_price
            product.price = new_price
            product.save()
            print(f"Updated {product.description} to new price {new_price}")  # Debugging statement



class ProductPriceDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = ProductPrice
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:productprice_list')
    permission_required = 'delete_productprice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Precio del Producto'
        context['description'] = f"¿Desea eliminar el precio del producto: {self.object.product.description}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.reset_product_prices(self.object)
        success_message = f"Éxito al eliminar el precio del producto {self.object.product.description}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

    def reset_product_prices(self, product_price):
        # Restablece el precio de los productos basados en el ProductPriceDetail asociado
        for detail in product_price.productPrice_detail.all():
            product = detail.product
            new_price = product.price - detail.increment
            product.price = new_price
            product.save()
