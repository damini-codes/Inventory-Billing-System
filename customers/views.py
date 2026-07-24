from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer

@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-date_added')
    return render(request, 'customers/customer_list.html', {'customers': customers})

@login_required
def customer_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        
        Customer.objects.create(
            name=name,
            phone_number=phone_number,
            email=email,
            address=address
        )
        messages.success(request, 'Customer added successfully!')
        return redirect('customer_list')
    return render(request, 'customers/customer_form.html', {'action': 'Add'})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.phone_number = request.POST.get('phone_number')
        customer.email = request.POST.get('email')
        customer.address = request.POST.get('address')
        customer.save()
        messages.success(request, 'Customer updated successfully!')
        return redirect('customer_list')
    return render(request, 'customers/customer_form.html', {'customer': customer, 'action': 'Edit'})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, 'Customer deleted successfully!')
    return redirect('customer_list')
