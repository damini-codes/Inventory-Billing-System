from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Category
from django.core.paginator import Paginator

@login_required
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventory/product_list.html', {'page_obj': page_obj, 'products': products})

@login_required
def product_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        purchase_price = request.POST.get('purchase_price')
        selling_price = request.POST.get('selling_price')
        quantity = request.POST.get('quantity')
        barcode = request.POST.get('barcode')
        gst_percent = request.POST.get('gst_percent')
        
        category = get_object_or_404(Category, id=category_id) if category_id else None
        
        Product.objects.create(
            name=name,
            category=category,
            purchase_price=purchase_price,
            selling_price=selling_price,
            quantity=quantity,
            barcode=barcode,
            gst_percent=gst_percent
        )
        messages.success(request, 'Product added successfully!')
        return redirect('product_list')
    
    categories = Category.objects.all()
    return render(request, 'inventory/product_form.html', {'categories': categories, 'action': 'Add'})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        category_id = request.POST.get('category')
        product.category = get_object_or_404(Category, id=category_id) if category_id else None
        product.purchase_price = request.POST.get('purchase_price')
        product.selling_price = request.POST.get('selling_price')
        product.quantity = request.POST.get('quantity')
        product.barcode = request.POST.get('barcode')
        product.gst_percent = request.POST.get('gst_percent')
        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('product_list')
    
    categories = Category.objects.all()
    return render(request, 'inventory/product_form.html', {'product': product, 'categories': categories, 'action': 'Edit'})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect('product_list')

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {'categories': categories})

@login_required
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Category.objects.create(name=name, description=description)
        messages.success(request, 'Category added successfully!')
        return redirect('category_list')
    return render(request, 'inventory/category_form.html', {'action': 'Add'})

@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.save()
        messages.success(request, 'Category updated successfully!')
        return redirect('category_list')
    return render(request, 'inventory/category_form.html', {'category': category, 'action': 'Edit'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('category_list')
