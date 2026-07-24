import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
import os
from xhtml2pdf import pisa
from inventory.models import Product
from .models import Invoice, InvoiceItem
from customers.models import Customer

def home(request):
    return render(request, 'billing/home.html')

@login_required
def billing_page(request):
    products = Product.objects.filter(quantity__gt=0)
    customers = Customer.objects.all()
    return render(request, 'billing/billing.html', {'products': products, 'customers': customers})

def search_product(request):
    if request.method == 'GET':
        query = request.GET.get('query', '').strip()
        
        try:
            product = Product.objects.get(barcode=query)
        except Product.DoesNotExist:
            try:
                product = Product.objects.get(name__icontains=query)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=404)
        
        product_data = {
            'id': product.id,
            'name': product.name,
            'selling_price': str(product.selling_price),
            'gst_percent': str(product.gst_percent),
            'quantity_in_stock': product.quantity,
        }
        return JsonResponse(product_data)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def save_invoice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        invoice_items_data = data.get('items', [])
        grand_total = data.get('grand_total')
        total_amount = data.get('total_amount')
        customer_id = data.get('customer_id')
        
        if not invoice_items_data or not grand_total:
            return JsonResponse({'error': 'Missing items or totals'}, status=400)
        
        try:
            with transaction.atomic():
                next_invoice_number = Invoice.objects.count() + 1
                invoice_num = f"INV-{next_invoice_number:05d}"
                
                customer = None
                if customer_id:
                    customer = Customer.objects.get(id=customer_id)
                
                invoice = Invoice.objects.create(
                    invoice_number=invoice_num,
                    customer=customer,
                    total_amount=total_amount,
                    grand_total=grand_total,
                )
                
                for item_data in invoice_items_data:
                    product_id = item_data.get('product_id')
                    qty = item_data.get('qty')
                    unit_price = item_data.get('price')
                    gst = item_data.get('gst')
                    
                    product = Product.objects.get(id=product_id)
                    
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        product=product,
                        quantity=qty,
                        unit_price=unit_price,
                        gst_percent=gst,
                    )
                    
                    product.quantity -= qty
                    product.save()
                
                invoice_data = {
                    'invoice': invoice,
                    'items': invoice.items.all(),
                }
                
                pdf_path = generate_invoice_pdf(invoice_data)
                
                customer_phone = customer.phone_number if customer else None
                
                return JsonResponse({
                    'message': 'Invoice saved successfully!', 
                    'invoice_number': invoice_num,
                    'invoice_id': invoice.id,
                    'pdf_path': pdf_path,
                    'customer_phone': customer_phone
                }, status=201)
        
        except Product.DoesNotExist:
            return JsonResponse({'error': 'One or more products not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'A database error occurred: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def generate_invoice_pdf(invoice_data):
    invoice = invoice_data['invoice']
    items = invoice_data['items']
    
    subtotal = 0
    total_gst = 0
    
    for item in items:
        base = float(item.unit_price) * item.quantity
        gst = base * (float(item.gst_percent) / 100)
        subtotal += base
        total_gst += gst
    
    context = {
        'invoice': invoice,
        'items': items,
        'subtotal': subtotal,
        'gst': total_gst,
        'grand_total': float(invoice.grand_total),
    }
    
    html_content = render_to_string('billing/invoice_pdf.html', context)
    
    media_root = settings.MEDIA_ROOT if hasattr(settings, 'MEDIA_ROOT') else os.path.join(os.path.dirname(__file__), '..', '..', 'media')
    os.makedirs(media_root, exist_ok=True)
    
    pdf_filename = f"Invoice_{invoice.invoice_number}.pdf"
    pdf_path = os.path.join(media_root, pdf_filename)
    
    with open(pdf_path, 'wb') as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    
    return pdf_filename

@login_required
def download_invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = invoice.items.all()
    
    subtotal = 0
    total_gst = 0
    
    for item in items:
        base = float(item.unit_price) * item.quantity
        gst = base * (float(item.gst_percent) / 100)
        subtotal += base
        total_gst += gst
    
    context = {
        'invoice': invoice,
        'items': items,
        'subtotal': subtotal,
        'gst': total_gst,
        'grand_total': float(invoice.grand_total),
    }
    
    html_content = render_to_string('billing/invoice_pdf.html', context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{invoice.invoice_number}.pdf"'
    
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    
    return response

@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-date')
    return render(request, 'billing/invoice_list.html', {'invoices': invoices})

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = invoice.items.all()
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice, 'items': items})
