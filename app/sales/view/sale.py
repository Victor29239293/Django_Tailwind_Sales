import json
from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse_lazy
from app.core.forms.supplier import SupplierForm
from app.core.models import Product , Company
from app.sales.form.invoice import InvoiceForm
from app.sales.models import Invoice, InvoiceDetail
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView,DetailView
from django.contrib import messages
from django.db.models import Q,F
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils import timezone
from django.shortcuts import redirect
from proy_sales.utils import custom_serializer, save_audit
# from reportlab.pdfgen import canvas
# from weasyprint import HTML
from django.http import HttpResponse
from io import BytesIO
# from reportlab.lib.pagesizes import letter
import os
# from reportlab.lib import colors
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Image,Spacer,HRFlowable
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.units import inch
from django.conf import settings
from datetime import timedelta

class SaleListView(PermissionMixin,ListViewMixin, ListView):
    template_name = 'sales/invoices/list.html'
    model = Invoice
    context_object_name = 'invoices'
    permission_required = 'view_invoice'
    paginate_by = 5
    def get_queryset(self):
        q1 = self.request.GET.get('q') # ver
        if q1 is not None: 
            self.query.add(Q(id = q1), Q.OR) 
            self.query.add(Q(customer__first_name__icontains=q1), Q.OR) 
            self.query.add(Q(customer__last_name__icontains=q1), Q.OR) 
        return self.model.objects.filter(self.query).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['permission_add'] = context['permissions'].get('add_supplier','')
        # context['create_url'] = reverse_lazy('core:supplier_create')
        return context
class SaleCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:invoice_list')
    permission_required = 'add_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'price', 'stock', 'iva__value')
        context['detail_sales'] = []
        context['save_url'] = reverse_lazy('sales:sales_create')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            messages.error(self.request, f"Error al grabar la venta: {form.errors}")
            return JsonResponse({"msg": form.errors}, status=400)
        
        data = request.POST
        try:
            with transaction.atomic():
                sale = Invoice.objects.create(
                    customer_id=int(data['customer']),
                    payment_method_id=int(data['payment_method']),
                    issue_date=data['issue_date'],
                    subtotal=Decimal(data['subtotal']),
                    discount=Decimal(data['discount']),
                    iva=Decimal(data['iva']),
                    total=Decimal(data['total']),
                    #payment=Decimal(data['payment']),
                    change=Decimal(data['change']),
                    state='F'
                )

                details = json.loads(request.POST['detail'])
                print("Details from POST request:", details)  # Debugging line
                for detail in details:
                    inv_det = InvoiceDetail.objects.create(
                        invoice=sale,
                        product_id=int(detail['id']),
                        quantity=Decimal(detail['quantity']),  # Ensure this is 'quantity' not 'quantify'
                        price=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),
                        subtotal=Decimal(detail['sub'])
                    )
                    inv_det.product.reduce_stock(Decimal(detail['quantity']))  # Ensure this is 'quantity' not 'quantify'

                save_audit(request, sale, "A")
                messages.success(self.request, f"Éxito al registrar la venta F#{sale.id}")
                return JsonResponse({"msg": "Éxito al registrar la venta Factura"}, status=200)
        except Exception as ex:
            return JsonResponse({"msg": str(ex)}, status=400)

class SaleUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Invoice
    template_name = 'sales/invoices/form.html'
    form_class = InvoiceForm
    success_url = reverse_lazy('sales:invoice_list')
    permission_required = 'change_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'price', 'stock', 'iva__value')
        detail_sale = list(InvoiceDetail.objects.filter(invoice_id=self.object.id).values(
            "product", "product__description", "quantity", "price", "subtotal", "iva"))
        detail_sale = json.dumps(detail_sale, default=custom_serializer)
        context['detail_sales'] = detail_sale
        context['save_url'] = reverse_lazy('sales:sales_update', kwargs={"pk": self.object.id})
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            messages.error(self.request, f"Error al actualizar la venta: {form.errors}")
            return JsonResponse({"msg": form.errors}, status=400)
        
        data = request.POST
        try:
            sale = Invoice.objects.get(id=self.kwargs.get('pk'))
            with transaction.atomic():
                sale.customer_id = int(data['customer'])
                sale.payment_method_id = int(data['payment_method'])
                sale.issue_date = data['issue_date']
                sale.subtotal = Decimal(data['subtotal'])
                sale.discount = Decimal(data['discount'])
                sale.iva = Decimal(data['iva'])
                sale.total = Decimal(data['total'])
                sale.payment = Decimal(data['payment'])
                sale.change = Decimal(data['change'])
                sale.state = 'M'
                sale.save()

                details = json.loads(request.POST['detail'])
                print("Details from POST request:", details)  # Debugging line
                InvoiceDetail.objects.filter(invoice_id=sale.id).delete()
                for detail in details:
                    inv_det = InvoiceDetail.objects.create(
                        invoice=sale,
                        product_id=int(detail['id']),
                        quantity=Decimal(detail['quantity']),  # Ensure this is 'quantity' not 'quantify'
                        price=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),
                        subtotal=Decimal(detail['sub'])
                    )
                    inv_det.product.reduce_stock(Decimal(detail['quantity']))  # Ensure this is 'quantity' not 'quantify'

                save_audit(request, sale, "M")
                messages.success(self.request, f"Éxito al modificar la venta F#{sale.id}")
                return JsonResponse({"msg": "Éxito al modificar la venta Factura"}, status=200)
        except Exception as ex:
            return JsonResponse({"msg": str(ex)}, status=400)


          
class SaleAnnulView(PermissionMixin, View):
    permission_required = 'annul_invoice'
    model = Invoice
    success_url = reverse_lazy('sales:sales_list')

    def post(self, request, *args, **kwargs):
        try:
            sale = Invoice.objects.get(id=self.kwargs.get('pk'))
            
            if sale.state == 'A':
                messages.error(self.request, "La venta ya está anulada.")
                return redirect('sales:sales_list')
            
            current_time = timezone.now()
            time_difference = current_time - sale.issue_date
            if time_difference > timedelta(days=3):
                messages.error(self.request, "La venta solo se puede anular dentro de los 3 días de su realización.")
                return redirect('sales:sales_list')
            
            with transaction.atomic():
                sale.state = 'A'  # Cambiar estado a "Anulado"
                sale.save()
                
                for detail in sale.detail.all():
                    detail.product.stock += detail.quantity  # Ajustar el stock del producto
                    detail.product.save()
                
                save_audit(request, sale, "A")
                messages.success(self.request, f"Éxito al anular la venta F#{sale.id}")
                return redirect('sales:sales_list')
        except Invoice.DoesNotExist:
            messages.error(self.request, "Venta no encontrada.")
            return redirect('sales:sales_list')
        except Exception as ex:
            messages.error(self.request, f"Error al anular la venta: {str(ex)}")
            return redirect('sales:sales_list')

        
class SaleDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    permission_required = 'delete_invoice'
    model = Invoice
    success_url = reverse_lazy('sales:sales_list')
    
    def post(self, request, *args, **kwargs):
        try:
            sale_instance = self.get_object()
            
            if sale_instance.issue_date.date() != timezone.now().date():
                messages.error(self.request, "La venta solo se puede eliminar el mismo día de su realización.")
                return redirect('sales:sales_list')
            
            with transaction.atomic():
                details = sale_instance.detail.all()
                
                for detail in details:
                    detail.product.stock += detail.quantity  # Ajustar el stock del producto
                    detail.product.save()
                
                details.delete()
                
                sale_instance.delete()  # Eliminación lógica
                
                save_audit(request, sale_instance, "False")
                messages.success(self.request, f"Éxito al eliminar la factura #{sale_instance.id}.")
                return redirect('sales:sales_list')
        except Invoice.DoesNotExist:
            messages.error(self.request, "Venta no encontrada.")
            return redirect('sales:sales_list')
        except Exception as ex:
            messages.error(self.request, f"Error al eliminar la venta: {str(ex)}")
            return redirect('sales:sales_list')
        
class SaleDetailView(PermissionMixin, DetailView):
    model = Invoice
    template_name = 'sales/invoices/detail.html'
    context_object_name = 'invoice'
    permission_required = 'view_invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = InvoiceDetail.objects.filter(invoice=self.object)
        context['company'] = Company.objects.first()
        context['customer'] = self.object.customer
        context['title1'] = 'IC - Invoices'
        context['title2'] = 'Detalle de la factura:'

        # Define colors for each state
        state_colors = {
            'F': 'bg-green-500 text-white',
            'Anulada': 'bg-red-500 text-white',
            'M': 'bg-orange-500 text-white',
        }

        # Get the state of the invoice and its color
        state = self.object.get_state_display()
        context['state_color'] = state_colors.get(state, 'bg-gray-500 text-white')
        
        return context


# class InvoicePrintView(View):

#     def get(self, request, *args, **kwargs):
#         invoice = get_object_or_404(Invoice, id=kwargs.get('pk'))
#         details = InvoiceDetail.objects.filter(invoice=invoice)

#         # Create a BytesIO buffer to receive the PDF data
#         buffer = BytesIO()
#         doc = SimpleDocTemplate(buffer, pagesize=letter)

#         # Styles
#         styles = getSampleStyleSheet()
#         title_style = ParagraphStyle(
#             'Title',
#             fontSize=24,
#             leading=28,
#             spaceAfter=12,
#             alignment=1,  # Center alignment
#             textColor=colors.darkblue,
#             fontName='Helvetica-Bold'
#         )
#         company_style = ParagraphStyle(
#             'Company',
#             fontSize=30,
#             leading=22,
#             spaceAfter=12,
#             alignment=1,  # Center alignment
#             textColor=colors.black,
#             fontName='Helvetica-Bold'
#         )
#         header_style = ParagraphStyle(
#             'Header',
#             fontSize=12,
#             leading=15,
#             spaceAfter=10,
#             alignment=0,
#             textColor=colors.black,
#             fontName='Helvetica'
#         )
#         footer_style = ParagraphStyle(
#             'Footer',
#             fontSize=10,
#             leading=12,
#             spaceAfter=6,
#             alignment=1,  # Center alignment
#             textColor=colors.gray,
#             fontName='Helvetica-Oblique'
#         )

#         # Title
#         title = Paragraph(f"Nº DE FACTURA: {invoice.id}", title_style)
#         company = Paragraph("SUPERMAXI", company_style)

#         # Logo
#         logo_path = os.path.join(settings.MEDIA_ROOT, 'supermaxi.jpg')  # Update this path to your logo's path
#         try:
#             logo = Image(logo_path, 1.5 * inch, 1.5 * inch)
#         except IOError:
#             logo = Paragraph("<b>LOGO NO DISPONIBLE</b>", header_style)

#         # Header Information
#         header_info = Table([
#             [logo, company]
#         ], colWidths=[1.5*inch, 6*inch])
#         header_info.setStyle(TableStyle([
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
#             ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
#         ]))

#         # Separator Line
#         separator = HRFlowable(width="100%", thickness=1, color=colors.darkblue)

#         invoice_info_table = Table([
#             [
#                 Paragraph(
#                     f"<b>Rojo Polo Paella Inc.</b><br/>"
#                     f"Carretera Muelle 38<br/>"
#                     f"37531 Ávila, Ávila<br/><br/>",
#                     header_style
#                 ),
#                 Paragraph(
#                     f"<b>FACTURAR A:</b><br/>"
#                     f"{invoice.customer.first_name} {invoice.customer.last_name}<br/>"
#                     f"<b>DIRECCION :</b><br/>"
#                     f"{invoice.customer.address}<br/><br/>",
#                     header_style
#                 ),
#                 Paragraph(
#                     f"<b>FECHA:</b> {invoice.issue_date.strftime('%d/%m/%Y')}<br/>"
#                     f"<b>Nº DE Factura:{invoice.id}</b> <br/>"
#                     f"<b>FECHA VENCIMIENTO:</b><br/><br/>",
#                     header_style
#                 )
#             ]
#         ], colWidths=[2.5*inch, 3*inch, 2.5*inch])

#         # Table Data
#         data = [["CANT.", "DESCRIPCIÓN", "PRECIO UNITARIO", "IMPORTE"]]
#         for detail in details:
#             data.append([
#                 detail.quantity,
#                 detail.product.description,
#                 f"{detail.price:.2f} €",
#                 f"{detail.quantity * detail.price:.2f} €"
#             ])

#         # Add subtotal, IVA, and total
#         data.append(["", "", "Subtotal", f"{invoice.subtotal:.2f} €"])
#         data.append(["", "", "IVA 21.0%", f"{invoice.iva:.2f} €"])
#         data.append(["", "", "TOTAL", f"{invoice.total:.2f} €"])

#         # Table Style
#         table_style = TableStyle([
#             ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#             ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
#             ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
#         ])

#         table = Table(data, colWidths=[1*inch, 4*inch, 1.5*inch, 1.5*inch])
#         table.setStyle(table_style)

#         # Footer
#         footer_info = Paragraph(
#             f"""
#             <b>CONDICIONES Y FORMA DE PAGO</b><br/>
#             El pago se realizará en un plazo de 15 días<br/>
#             Banco Santander<br/>
#             IBAN: ES12 3456 7891<br/>
#             SWIFT/BIC: ABCDESM1XXX<br/>
#             <br/>
#             Gracias por su negocio.
#             """,
#             footer_style
#         )

#         # Build PDF
#         elements = [header_info, Spacer(1, 12), separator, Spacer(1, 12), invoice_info_table, Spacer(1, 12), table, Spacer(1, 12), separator, Spacer(1, 12), footer_info]
#         doc.build(elements)

#         # Seek to the beginning of the BytesIO buffer
#         buffer.seek(0)

#         # Create the HttpResponse and set the content type and Content-Disposition header
#         response = HttpResponse(buffer, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.id}.pdf"'
#         return response