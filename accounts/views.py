from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def dashboard(request):
    from inventory.models import Product
    from billing.models import Invoice
    from customers.models import Customer
    
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(quantity__lt=10).count()
    total_customers = Customer.objects.count()
    total_invoices = Invoice.objects.count()
    
    recent_invoices = Invoice.objects.order_by('-date')[:5]
    recent_products = Product.objects.order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'total_customers': total_customers,
        'total_invoices': total_invoices,
        'recent_invoices': recent_invoices,
        'recent_products': recent_products,
    }
    return render(request, 'accounts/dashboard.html', context)
