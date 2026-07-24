from django.contrib import admin
# Import the models you created (Product and Category)
from .models import Product, Category 

# Register them so they appear in the Admin Panel
admin.site.register(Product)
admin.site.register(Category)
