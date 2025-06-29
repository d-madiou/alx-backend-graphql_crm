# crm/seed_db.py
from crm.models import Customer, Product

Customer.objects.create(name="Alice", email="alice@example.com", phone="+1234567890")
Product.objects.create(name="Mouse", price=15.0, stock=10)
