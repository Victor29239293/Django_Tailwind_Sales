from django.urls import path
from app.core.views import supplier , brands , Customer , categoria,productos, linea ,payment_method,product_price, iva , company
 
app_name='core' # define un espacio de nombre para la aplicación
urlpatterns = [    
    # URLs de proveedores
    path('supplier_list/', supplier.SupplierListView.as_view() ,name='supplier_list'),
    path('supplier_create/', supplier.SupplierCreateView.as_view(),name='supplier_create'),
    path('supplier_update/<int:pk>/', supplier.SupplierUpdateView.as_view(),name='supplier_update'),
    path('supplier_delete/<int:pk>/', supplier.SupplierDeleteView.as_view(),name='supplier_delete'),
    path('views_maps/', supplier.Views_Maps.as_view(),name='views_maps'),
    #URLS de marcas
    path('brands_list/', brands.BrandListView.as_view(),name='brand_list'),
    path('brands_create/', brands.BrandCreateView.as_view(), name='brand_create'),
    path('brands_update/<int:pk>/', brands.BrandUpdateView.as_view(),name='brand_update'),
    path('brands_delete/<int:pk>/', brands.BrandDeleteView.as_view(),name='brand_delete'),
    #URLS DE CLIENTES
    path('customers_list/', Customer.CustomerListView.as_view(),name='customer_list'),
    path('api/obtener_datos_cedula/', Customer.obtener_datos_cedula, name='obtener_datos_cedula'),
    path('customers_create/', Customer.CustomerCreateView.as_view(), name='customer_create'),
    path('customers_view/<int:pk>/', Customer.CustomerDetailView.as_view(), name='customer_view'),
    path('customers_update/<int:pk>/', Customer.CustomerUpdateView.as_view(),name='customer_update'),
    path('customers_delete/<int:pk>/', Customer.CustomerDeleteView.as_view(),name='customer_delete'),
    
    #URLS DE CATEGORIA
    path('category_list/', categoria.CategoriaListView.as_view(),name='category_list'),
    path('category_create/', categoria.CategoriaCreateView.as_view(), name='category_create'),
    # path('categoria_view/<int:pk>/', Customer.CustomerDetailView.as_view(), name='customer_view'),
    path('category_update/<int:pk>/', categoria.CategoriaUpdateView.as_view(),name='category_update'),
    path('category_delete/<int:pk>/', categoria.CategoriaDeleteView.as_view(),name='category_delete'),
    
     # URLs de productos
    path('products_list/', productos.ProductListView.as_view(), name='product_list'),
    path('products_create/', productos.ProductCreateView.as_view(), name='product_create'),
    path('products_update/<int:pk>/', productos.ProductUpdateView.as_view(), name='product_update'),
    path('products_delete/<int:pk>/', productos.ProductDeleteView.as_view(), name='product_delete'),
     # URLs de líneas
    path('lines_list/', linea.LineListView.as_view(), name='line_list'),
    path('lines_create/', linea.LineCreateView.as_view(), name='line_create'),
    path('lines_update/<int:pk>/', linea.LineUpdateView.as_view(), name='line_update'),
    path('lines_delete/<int:pk>/', linea.LineDeleteView.as_view(), name='line_delete'),
    
    # URLs de métodos de pago
    path('payment_methods_list/', payment_method.PaymentMethodListView.as_view(), name='payment_method_list'),
    path('payment_methods_create/', payment_method.PaymentMethodCreateView.as_view(), name='payment_method_create'),
    path('payment_methods_update/<int:pk>/', payment_method.PaymentMethodUpdateView.as_view(), name='payment_method_update'),
    path('payment_methods_delete/<int:pk>/', payment_method.PaymentMethodDeleteView.as_view(), name='payment_method_delete'),
    # URLs de precios de productos
    path('product_prices_list/', product_price.ProductPriceListView.as_view(), name='productprice_list'),
    path('product_prices_create/', product_price.ProductPriceCreateView.as_view(), name='productprice_create'),
    path('product_prices_update/<int:pk>/', product_price.ProductPriceUpdateView.as_view(), name='productprice_update'),
    path('product_prices_delete/<int:pk>/', product_price.ProductPriceDeleteView.as_view(), name='productprice_delete'),
    # URLs de precios de Iva
    path('iva_list/', iva.IvaListView.as_view(), name='iva_list'),
    path('iva_create/', iva.IvaCreateView.as_view(), name='iva_create'),
    path('iva_update/<int:pk>/', iva.IvaUpdateView.as_view(), name='iva_update'),
    path('iva_delete/<int:pk>/', iva.IvaDeleteView.as_view(), name='iva_delete'),
    # URLs de precios de Company
    path('company_list/', company.CompanyListView.as_view(), name='company_list'),
    path('company_create/', company.CompanyCreateView.as_view(), name='company_create'),
    path('company_update/<int:pk>/', company.CompanyUpdateView.as_view(), name='company_update'),
    path('company_delete/<int:pk>/', company.CompanyDeleteView.as_view(), name='company_delete'),

 ]

    # Otras URLs
#     path('signup/', views.signup, name='signup'),
#     path('logout/', views.signout, name='logout'),
#     path('signin/', views.signin, name='signin'),

#     # URLs de productos
#     path('product_list/', views.product_List,name='product_list'),
#     path('product_create/', views.product_create,name='product_create'),
#     path('product_update/<int:id>/', views.product_update,name='product_update'),
#     path('product_delete/<int:id>/', views.product_delete,name='product_delete'),

#     # URLs de marcas
#     path('brand_list/', views.brand_List,name='brand_list'),
#     path('brand_create/', views.brand_create,name='brand_create'),
#     path('brand_update/<int:id>/', views.brand_update,name='brand_update'),
#     path('brand_delete/<int:id>/', views.brand_delete,name='brand_delete'),


#     # URLs de categorías
#     path('category_list/', views.category_List,name='category_list'),
#     path('category_create/', views.category_create,name='category_create'),
#     path('category_update/<int:id>/', views.category_update,name='category_update'),
#     path('category_delete/<int:id>/', views.category_delete,name='category_delete'),
    
#     path('purchase/', include('app.purchase.urls')),
# 
