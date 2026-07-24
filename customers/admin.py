from django.contrib import admin
from .models import Customer # Import the Customer model you just created

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'is_active', 'date_added')
    search_fields = ('name', 'phone_number', 'email')
    list_filter = ('is_active', 'date_added')

admin.site.register(Customer, CustomerAdmin)
