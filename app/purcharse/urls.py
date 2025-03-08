from django.urls import path
from app.purcharse.view import buys
 
app_name='purcharse' # define un espacio de nombre para la aplicación
urlpatterns = [    
    # URLs de proveedores
    path('purcharse_list/', buys.PurchaseListView.as_view() ,name='purcharse_list'),
    path('purcharse_create/', buys.PurchaseCreateView.as_view(),name='purcharse_create'),
    path("purchase_update/<int:pk>/", buys.PurchaseUpdateView.as_view(), name="purchase_update"),   
    path('purchase_detail/<int:pk>/', buys.PurchaseDetailView.as_view(),name='purchase_detail'),
    path('purchase/annul/<int:pk>/', buys.PurchaseAnnulView.as_view(), name='purchase_annul'),
    path('purcharse/delete/<int:pk>/', buys.PurchaseDeleteView.as_view(), name='purchase_delete'),
    # path("purchase_pdf/<int:pk>/", buys.PurchaseGenerateInvoiceView.as_view(), name="purchase_pdf"),
    
    # path('supplier_delete/<int:pk>/', supplier.SupplierDeleteView.as_view(),name='supplier_delete'),
 ]