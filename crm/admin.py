from django.contrib import admin

# Register your models here.
# crm/admin.py
from .models import Customer, Product, Order
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
