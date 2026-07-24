from django.db import models

# --- 1. Invoice Model (The Header/Summary) ---
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)

    # Use string reference to link to the Customer model
    customer = models.ForeignKey(
        'customers.Customer', 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)  
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

# --- 2. Invoice Item Model ---
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    gst_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def total(self):
        base_total = self.unit_price * self.quantity
        gst_amount = base_total * (self.gst_percent / 100)
        return base_total + gst_amount

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"