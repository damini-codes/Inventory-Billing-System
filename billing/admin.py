from django.contrib import admin
from .models import Invoice, InvoiceItem

# --- 1. Inline Class for displaying items inside the Invoice ---
class InvoiceItemInline(admin.TabularInline):
    # This connects InvoiceItem to Invoice
    model = InvoiceItem
    extra = 0  # Do not show extra empty forms for adding new items
    
    # Set fields in the inline view to read-only
    readonly_fields = [
        'product', 
        'quantity', 
        'unit_price', 
        'gst_percent'
    ]
    
    # Do NOT exclude 'invoice' as it's the required foreign key (Fixes E201 error)
    
    
# --- 2. Custom Admin for Invoice (Read-Only Header) ---
class InvoiceAdmin(admin.ModelAdmin):
    # These fields can be viewed but CANNOT be changed once saved
    readonly_fields = [
        'invoice_number', 
        'date', 
        'customer',
        'total_amount',
        'grand_total',
    ]

    # Display these fields on the list page
    list_display = (
        'invoice_number', 
        'customer', 
        'grand_total', 
        'date'
    )

    # Allow searching by invoice number or customer name
    search_fields = (
        'invoice_number', 
        'customer__name',
        'customer__phone_number'
    )
    
    # Include the line items at the bottom of the Invoice page
    inlines = [InvoiceItemInline]


# --- 3. Custom Admin for InvoiceItem (Makes the separate link read-only) ---
class InvoiceItemAdmin(admin.ModelAdmin):
    # Set all fields to read-only for the main 'Invoice items' view
    readonly_fields = [
        'invoice',        
        'product',        
        'quantity',       
        'unit_price',     
        'gst_percent',    
    ]
    list_display = (
        'invoice', 
        'product', 
        'quantity', 
        'unit_price'
    )
    search_fields = (
        'invoice__invoice_number', 
        'product__name'
    )


# --- 4. Register Models ---

# Register Invoice using the custom InvoiceAdmin class
admin.site.register(Invoice, InvoiceAdmin)

# Register the InvoiceItem model using the custom read-only InvoiceItemAdmin
admin.site.register(InvoiceItem, InvoiceItemAdmin) 