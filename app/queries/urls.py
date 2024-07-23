from django.urls import path
from app.queries.views import query

app_name = 'queries'  # define un espacio de nombre para la aplicación
urlpatterns = [
    # URLs de consultas
    path('query_sales/', query.QuerySalesListView.as_view(), name='query_sales'),
    path('query_purchase/', query.QueryPurchaseListView.as_view(), name='query_purchase'),
    #path('sales_detail/<int:pk>/', query.SaleDetailView.as_view(),name='sales_detail'),
]

