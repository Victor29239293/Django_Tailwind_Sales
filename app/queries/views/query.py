from django.core.serializers.json import DjangoJSONEncoder
import decimal
import json
from collections import defaultdict
from app.sales.models import Invoice
from app.purcharse.models import Purchase
from app.security.mixins.mixins import ListViewMixin, PermissionMixin
from django.views.generic import ListView
from django.db.models import Q



class QuerySalesListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'queries/query_sales.html'
    model = Invoice
    context_object_name = 'invoices'
    permission_required = 'view_invoice'

    def get_queryset(self):
        query = Q()
        id = self.request.GET.get('id')
        customer = self.request.GET.get('customer')
        payment_method = self.request.GET.get('payment_method')
        issue_date = self.request.GET.get('issue_date')
        subtotal = self.request.GET.get('subtotal')
        discount = self.request.GET.get('discount')
        total = self.request.GET.get('total')
        state = self.request.GET.get('state')
        active = self.request.GET.get('active')

        if id:
            query &= Q(id=id)
        if customer:
            query &= Q(customer__first_name__icontains=customer) | Q(customer__last_name__icontains=customer)
        if payment_method:
            query &= Q(payment_method__description__icontains=payment_method)
        if issue_date:
            query &= Q(issue_date=issue_date)
        if subtotal:
            query &= Q(subtotal__icontains=subtotal)
        if discount:
            query &= Q(discount__icontains=discount)
        if total:
            query &= Q(total__icontains=total)
        if state:
            query &= Q(state__icontains=state)
        if active:
            query &= Q(active__icontains=active)

        return self.model.objects.filter(query).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'IC - Queries'
        context['title2'] = 'Consulta de ventas en tablas y gráficos.'
        context['title3'] = 'Consulta de ventas.'
        
        sales = self.get_queryset()

        labels = []
        totals = []

        monthly_sales = defaultdict(int)
        customer_sales = defaultdict(int)
        sales_by_hour = defaultdict(int)
        product_sales = defaultdict(int)

        for sale in sales:
            formatted_date = sale.issue_date.strftime('%d-%m-%Y')
            labels.append(formatted_date)
            totals.append(float(sale.total))
            
            month = sale.issue_date.strftime('%Y-%m')
            monthly_sales[month] += 1
            
            customer_name = f"{sale.customer.first_name} {sale.customer.last_name}"
            customer_sales[customer_name] += 1
            
            hour = sale.issue_date.strftime('%H')
            sales_by_hour[hour] += 1

            for item in sale.detail.all(): 
                product_sales[item.product.description] += int(item.quantity)

        chart_data = {
            'labels': labels,
            'totals': totals,
        }

        monthly_sales_data = {
            'labels': list(monthly_sales.keys()),
            'totals': [float(total) for total in monthly_sales.values()]
        }
        
        customer_sales_data = {
            'customers': list(customer_sales.keys()),
            'sales_counts': list(customer_sales.values())
        }

        sales_by_hour_data = {
            'labels': [f"{hour}:00" for hour in sorted(sales_by_hour.keys())],
            'totals': [sales_by_hour[hour] for hour in sorted(sales_by_hour.keys())]
        }

        product_sales_data = {
            'products': list(product_sales.keys()),
            'quantities': list(product_sales.values())
        }

        # Debug print
        print("product_sales_data:", product_sales_data)

        context['chart_data'] = json.dumps(chart_data)
        context['monthly_sales'] = json.dumps(monthly_sales_data)
        context['customer_sales_data'] = json.dumps(customer_sales_data)
        context['sales_by_hour_data'] = json.dumps(sales_by_hour_data)
        context['product_sales_data'] = json.dumps(product_sales_data)
        
        return context
    
    
    

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super().default(obj)

class QueryPurchaseListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'queries/query_purchase.html'
    model = Purchase
    context_object_name = 'purchases'
    permission_required = 'view_purchase'
    
    def get_queryset(self):
        query = Q()
        num_document = self.request.GET.get('num_document')
        supplier = self.request.GET.get('supplier')
        issue_date = self.request.GET.get('issue_date')
        subtotal = self.request.GET.get('subtotal')
        total = self.request.GET.get('total')
        active = self.request.GET.get('active')

        if num_document:
            query &= Q(id=num_document)
        if supplier:
            query &= Q(supplier__name__icontains=supplier)
        if issue_date:
            query &= Q(issue_date=issue_date)
        if subtotal:
            query &= Q(subtotal__icontains=subtotal)
        if total:
            query &= Q(total__icontains=total)
        if active:
            query &= Q(active__icontains=active)

        return self.model.objects.filter(query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title1'] = 'IC - Queries'
        context['title2'] = 'Consulta de compras en tablas y gráficos.'
        context['title3'] = 'Consulta de Compras.'
        
        # Data for charts
        purchases = self.get_queryset()

        labels = []
        totals = []

        monthly_purchases = defaultdict(int)
        supplier_purchase = defaultdict(int)
        product_purchase = defaultdict(int)

        for purchase in purchases:
            formatted_date = purchase.issue_date.strftime('%d-%m-%Y')
            labels.append(formatted_date)
            totals.append(float(purchase.total))
            
            month = purchase.issue_date.strftime('%Y-%m')
            monthly_purchases[month] += 1
            
            supplier_name = f"{purchase.supplier.name}"
            supplier_purchase[supplier_name] += 1
            
            for item in purchase.purchase_detail.all():  # Corrección aquí
                product_purchase[item.product.description] += int(item.quantify)

        chart_data = {
            'labels': labels,
            'totals': totals,
        }

        monthly_purchases_data = {
            'labels': list(monthly_purchases.keys()),
            'totals': [float(total) for total in monthly_purchases.values()]
        }
        
        supplier_purchases_data = {
            'suppliers': list(supplier_purchase.keys()),
            'purchases_counts': list(supplier_purchase.values())
        }
        
        product_purchases_data = {
            'products': list(product_purchase.keys()),
            'quantities': list(product_purchase.values())
        }
        
        # Debug print
        print("supplier_purchases_data:", supplier_purchases_data)
        print("product_purchases_data:", product_purchases_data)
        
        context['chart_data'] = json.dumps(chart_data)
        context['monthly_purchases'] = json.dumps(monthly_purchases_data)
        context['supplier_purchases_data'] = json.dumps(supplier_purchases_data)
        context['product_purchases_data'] = json.dumps(product_purchases_data)
        
        return context

