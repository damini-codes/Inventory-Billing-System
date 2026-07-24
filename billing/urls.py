from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('billing/', views.billing_page, name='billing'),
    path('billing/invoices/', views.invoice_list, name='invoice_list'),
    path('billing/invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('billing/invoices/<int:pk>/pdf/', views.download_invoice_pdf, name='download_invoice_pdf'),
    path('search_product/', views.search_product, name='search_product'),
    path('save_invoice/', views.save_invoice, name='save_invoice'),
]
