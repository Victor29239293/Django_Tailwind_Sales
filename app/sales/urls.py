from django.urls import path
from app.sales.view import sale
 
app_name='sales' # define un espacio de nombre para la aplicación
urlpatterns = [    
    # URLs de proveedores
    path('sales_list/', sale.SaleListView.as_view() ,name='sales_list'),
    path('sales_create/', sale.SaleCreateView.as_view(),name='sales_create'),
    path('sales_update/<int:pk>/', sale.SaleUpdateView.as_view(),name='sales_update'),
    path('sales_detail/<int:pk>/', sale.SaleDetailView.as_view(),name='sales_detail'),
    path('sales/annul/<int:pk>/', sale.SaleAnnulView.as_view(), name='sales_annul'),
    path('sales/delete/<int:pk>/', sale.SaleDeleteView.as_view(), name='sales_delete'),
    # path('invoice/print/<int:pk>/', sale.InvoicePrintView.as_view(), name='invoice_print'),


    # path('supplier_delete/<int:pk>/', supplier.SupplierDeleteView.as_view(),name='supplier_delete'),
 ]