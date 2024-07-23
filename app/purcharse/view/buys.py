import json
from django.http import JsonResponse
from django.db import transaction
from django.urls import reverse_lazy
from app.core.forms.supplier import SupplierForm
from app.core.models import Product, Company
from app.purcharse.forms.buys import PurchaseForm
from app.purcharse.models import Purchase, PurchaseDetail
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.db.models import Q, F
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils import timezone
from django.shortcuts import redirect
from proy_sales.utils import custom_serializer, save_audit
from reportlab.lib.pagesizes import letter
from weasyprint import HTML
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.conf import settings
import os
from arrow import now
from django.db import IntegrityError
from datetime import timedelta

class PurchaseListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'purchase/buys/list.html'
    model = Purchase
    context_object_name = 'purchases'
    permission_required = 'view_purchase'

    def get_queryset(self):
        query = Q()
        q1 = self.request.GET.get('q')
        if q1 is not None:
            query.add(Q(id=q1), Q.OR)
            query.add(Q(supplier__name__icontains=q1), Q.OR)
        return self.model.objects.filter(query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
class PurchaseCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Purchase
    template_name = 'purchase/buys/form.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purcharse:purcharse_list')
    permission_required = 'add_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'price', 'stock', 'iva__value')
        context['detail_purchases'] = []
        context['save_url'] = reverse_lazy('purcharse:purcharse_create')
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            messages.success(self.request, f"Error al registrar la compra: {form.errors}.")
            return JsonResponse({"msg": form.errors}, status=400)
        data = request.POST
        try:
            with transaction.atomic():
                purchase = Purchase.objects.create(
                    supplier_id=int(data['supplier']),
                    issue_date=data['issue_date'],
                    subtotal=Decimal(data['subtotal']),
                    iva=Decimal(data['iva']),
                    total=Decimal(data['total'])
                )
                details = json.loads(request.POST['detail'])
                for detail in details:
                    product = Product.objects.get(id=int(detail['id']))
                    product.stock += Decimal(detail['quantify'])
                    product.save()
                    PurchaseDetail.objects.create(
                        purchase=purchase,
                        product=product,
                        quantify=Decimal(detail['quantify']),
                        cost=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),
                        subtotal=Decimal(detail['sub'])
                    )
                save_audit(request, purchase, "A")
                messages.success(self.request, f"Éxito al registrar la compra N#{purchase.id}")
                return JsonResponse({"msg": "Éxito al registrar la compra"}, status=200)
        except Exception as ex:
            return JsonResponse({"msg": str(ex)}, status=400)
class PurchaseUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Purchase
    template_name = 'purchase/buys/form.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purcharse:purchase_list')
    permission_required = 'change_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.active_products.values('id', 'description', 'price', 'stock', 'iva__value')
        detail_purchase = list(PurchaseDetail.objects.filter(purchase_id=self.object.id).values(
            "product", "product__description", "quantify", "cost", "subtotal", "iva"))
        detail_purchase = json.dumps(detail_purchase, default=custom_serializer)
        context['detail_purchases'] = detail_purchase
        context['save_url'] = reverse_lazy('purcharse:purchase_update', kwargs={"pk": self.object.id})
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid():
            messages.success(self.request, f"Error al actualizar la compra: {form.errors}.")
            return JsonResponse({"msg": form.errors}, status=400)
        data = request.POST
        try:
            purchase = Purchase.objects.get(id=self.kwargs.get('pk'))
            with transaction.atomic():
                purchase.num_document = data["num_document"]
                purchase.supplier_id = int(data['supplier'])
                purchase.issue_date = data['issue_date']
                purchase.subtotal = Decimal(data['subtotal'])
                purchase.iva = Decimal(data['iva'])
                purchase.total = Decimal(data['total'])
                purchase.save()

                # Restablecer el stock de productos a su estado anterior
                detdelete = PurchaseDetail.objects.filter(purchase_id=purchase.id)
                for det in detdelete:
                    det.product.stock -= int(det.quantify)
                    det.product.save()
                detdelete.delete()

                details = json.loads(request.POST['detail'])
                for detail in details:
                    product = Product.objects.get(id=int(detail['id']))
                    product.stock += Decimal(detail['quantify'])
                    product.save()
                    PurchaseDetail.objects.create(
                        purchase=purchase,
                        product=product,
                        quantify=Decimal(detail['quantify']),
                        cost=Decimal(detail['price']),
                        iva=Decimal(detail['iva']),
                        subtotal=Decimal(detail['sub'])
                    )
                save_audit(request, purchase, "M")
                messages.success(self.request, f"Éxito al modificar la compra N#{purchase.id}")
                return JsonResponse({"msg": "Éxito al modificar la compra"}, status=200)
        except Exception as ex:
            return JsonResponse({"msg": str(ex)}, status=400)
        
class PurchaseAnnulView(PermissionMixin, View):
    permission_required = 'annul_purchase'
    model = Purchase
    success_url = reverse_lazy('purcharse:purcharse_list')
    def post(self, request, *args, **kwargs):
        try:
            purchase = Purchase.objects.get(id=self.kwargs.get('pk'))
            
            if purchase.state == 'A':
                messages.error(self.request, "La compra ya está anulada")
                return redirect('purcharse:purcharse_list')
            
            current_time = timezone.now()
            time_difference = current_time - purchase.issue_date
            if time_difference > timedelta(days=3):
                messages.error(self.request, "La compra ya no puede ser anulada, pasaron los días establecidos")
                return redirect('purcharse:purcharse_list')
            
            with transaction.atomic():
                purchase.state = 'A'  # Cambiar estado a "Anulado"
                purchase.save()
                
                details = PurchaseDetail.objects.filter(purchase_id=purchase.id)
                for detail in details:
                    product = detail.product
                    product.stock -= detail.quantify  # Ajustar el stock del producto
                    product.save()
                    
                save_audit(request, purchase, "A")
                messages.success(self.request, f"Éxito al anular la compra #{purchase.id}")
                return redirect('purcharse:purcharse_list')
                
        except Purchase.DoesNotExist:
            messages.error(self.request, "Compra no encontrada")
            return redirect('purcharse:purcharse_list')
        except Exception as ex:
            return JsonResponse({"msg": str(ex)}, status=400)

class PurchaseDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    permission_required = 'delete_purchase'
    model = Purchase
    success_url = reverse_lazy('purcharse:purcharse_list')
    
    def post(self, request, *args, **kwargs):
        try:
            purchase_instance = self.get_object()
            
            # Verificar si la fecha de emisión es la misma que la fecha actual
            if purchase_instance.issue_date.date() != now().date():
                messages.error(request, "Solo se pueden eliminar las compras emitidas el día de hoy.")
                return redirect('purcharse:purcharse_list')
            
            with transaction.atomic():
                purchase_details = PurchaseDetail.objects.filter(purchase_id=purchase_instance.id)
                
                # Ajustar el stock de los productos primero
                for item in purchase_details:
                    product_instance = item.product
                    product_instance.stock -= item.quantify
                    product_instance.save()
                
                # Eliminar los detalles de la compra
                purchase_details.delete()
                
                # Marcar la compra como inactiva (eliminación lógica)
                purchase_instance.active = False
                purchase_instance.save()
                
                save_audit(request, purchase_instance, "False")
                messages.success(request, f"Éxito al eliminar la compra N#{purchase_instance.id}")
                return redirect('purcharse:purcharse_list') 
        except Purchase.DoesNotExist:
            messages.error(self.request, "La compra no existe.")
            return redirect('purcharse:purcharse_list') 
        except IntegrityError as ex:
            return JsonResponse({"msg": f"Error de integridad: {str(ex)}"}, status=400)
        except Exception as ex:
            return JsonResponse({"msg": str(ex)}, status=400)


class PurchaseDetailView(PermissionMixin, DetailView):
    model = Purchase
    template_name = 'purchase/buys/detail.html'
    context_object_name = 'purchase'
    permission_required = 'view_purchase'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['details'] = PurchaseDetail.objects.filter(purchase=self.object)
        context['company'] = Company.objects.first()
        
        # Define colors for each state
        state_colors = {
            'Normal': 'bg-green-500 text-white',
            'Pendiente': 'bg-orange-500 text-white',
            'Cancelado': 'bg-red-500 text-white',
        }

        # Get the state of the purchase and its color
        state = self.object.get_state_display()
        context['state_color'] = state_colors.get(state, 'bg-gray-500 text-white')
        
        return context
class PurchaseGenerateInvoiceView(PermissionMixin, View):
    permission_required = 'generate_invoice'

    def get(self, request, *args, **kwargs):
        # Obtener la compra
        purchase = get_object_or_404(Purchase, id=kwargs.get('pk'))
        details = PurchaseDetail.objects.filter(purchase=purchase)

        # Crear un buffer BytesIO para recibir los datos del PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'Title',
            fontSize=24,
            leading=28,
            spaceAfter=12,
            alignment=1,  # Alineación centrada
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        company_style = ParagraphStyle(
            'Company',
            fontSize=30,
            leading=22,
            spaceAfter=12,
            alignment=1,  # Alineación centrada
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
        header_style = ParagraphStyle(
            'Header',
            fontSize=12,
            leading=15,
            spaceAfter=10,
            alignment=0,
            textColor=colors.black,
            fontName='Helvetica'
        )
        footer_style = ParagraphStyle(
            'Footer',
            fontSize=10,
            leading=12,
            spaceAfter=6,
            alignment=1,  # Alineación centrada
            textColor=colors.gray,
            fontName='Helvetica-Oblique'
        )

        # Título
        title = Paragraph(f"Nº DE COMPRA: {purchase.id}", title_style)
        company = Paragraph("Supermaxi", company_style)

        # Logo
        logo_path = os.path.join(settings.MEDIA_ROOT, 'supermaxi.jpg')  # Actualiza esta ruta a la del logo
        try:
            logo = Image(logo_path, 1.5 * inch, 1.5 * inch)
        except IOError:
            logo = Paragraph("<b>LOGO NO DISPONIBLE</b>", header_style)

        # Información del encabezado
        header_info = Table([
            [logo, company]
        ], colWidths=[1.5 * inch, 6 * inch])
        header_info.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))

        # Línea separadora
        separator = HRFlowable(width="100%", thickness=1, color=colors.darkblue)

        # Información de la compra
        invoice_info_table = Table([
            [
                Paragraph(
                    f"<b>Dirección de la Empresa:</b><br/>"
                    f"Carretera Muelle 38<br/>"
                    f"37531 Ávila, Ávila<br/><br/>",
                    header_style
                ),
                Paragraph(
                    f"<b>Proovedor:</b><br/>"
                    f"{purchase.supplier.name}<br/>"
                    f"<b>DIRECCIÓN:</b><br/>"
                    f"{purchase.supplier.address}<br/><br/>",
                    header_style
                ),
                Paragraph(
                    f"<b>FECHA:</b> {purchase.issue_date.strftime('%d/%m/%Y %H:%M:%S')}<br/>"
                    f"<b>DETALLE DE COMPRA</b><br/>"
                    f"<b>Nº :</b> {purchase.id}<br/>",
                    
                    header_style
                )
            ]
        ], colWidths=[2.5 * inch, 3 * inch, 2.5 * inch])

        # Datos de la tabla
        data = [["CANT.", "DESCRIPCIÓN", "PRECIO UNITARIO", "IMPORTE"]]
        for detail in details:
            data.append([
                detail.quantify,
                detail.product.description,
                f"{detail.cost:.2f} €",
                f"{detail.quantify * detail.cost:.2f} €"
            ])

        # Añadir subtotal, IVA y total
        data.append(["", "", "Subtotal", f"{purchase.subtotal:.2f} €"])
        data.append(["", "", "IVA 21.0%", f"{purchase.iva:.2f} €"])
        data.append(["", "", "TOTAL", f"{purchase.total:.2f} €"])

        # Estilo de la tabla
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
        ])

        table = Table(data, colWidths=[1 * inch, 4 * inch, 1.5 * inch, 1.5 * inch])
        table.setStyle(table_style)

        # Pie de página
        footer_info = Paragraph(
            f"""
            <b>CONDICIONES Y FORMA DE PAGO</b><br/>
            El pago se realizará en un plazo de 15 días<br/>
            Banco Santander<br/>
            IBAN: ES12 3456 7891<br/>
            SWIFT/BIC: ABCDESM1XXX<br/>
            <br/>
            Gracias por su negocio.
            """,
            footer_style
        )

        # Construir el PDF
        elements = [header_info, Spacer(1, 12), separator, Spacer(1, 12), invoice_info_table, Spacer(1, 12), table, Spacer(1, 12), separator, Spacer(1, 12), footer_info]
        doc.build(elements)

        # Volver al principio del buffer BytesIO
        buffer.seek(0)

        # Crear la respuesta HttpResponse y establecer el tipo de contenido y el encabezado Content-Disposition
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{purchase.id}.pdf"'
        return response