import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.db import IntegrityError, transaction
from datetime import datetime
from graphql import GraphQLError

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer

class ProductType(DjangoObjectType):
    class Meta:
        model = Product

class OrderType(DjangoObjectType):
    class Meta:
        model = Order

# Mutation: CreateCustomer
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if Customer.objects.filter(email=email).exists():
            raise GraphQLError("Email already exists.")
        customer = Customer.objects.create(name=name, email=email, phone=phone)
        return CreateCustomer(customer=customer, message="Customer created successfully")

# Mutation: BulkCreateCustomers
class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(graphene.JSONString)

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, input):
        customers = []
        errors = []
        for item in input:
            try:
                c = Customer.objects.create(**item)
                customers.append(c)
            except Exception as e:
                errors.append(f"{item.get('email') or item.get('name')}: {str(e)}")
        return BulkCreateCustomers(customers=customers, errors=errors)

# Mutation: CreateProduct
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int()

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0 or stock < 0:
            raise GraphQLError("Invalid price or stock value")
        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(product=product)

# Mutation: CreateOrder
class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.String()

    order = graphene.Field(OrderType)

    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(id=customer_id)
            products = Product.objects.filter(id__in=product_ids)
            if not products:
                raise GraphQLError("No valid products found.")
            total = sum([p.price for p in products])
            order = Order.objects.create(customer=customer, total_amount=total)
            order.products.set(products)
            if order_date:
                order.order_date = order_date
                order.save()
            return CreateOrder(order=order)
        except Customer.DoesNotExist:
            raise GraphQLError("Invalid customer ID")
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    

class Query(graphene.ObjectType):
    all_customers = graphene.List(CustomerType)
    def resolve_all_customers(self, info):
        return Customer.objects.all()
    all_products = graphene.List(ProductType)
    def resolve_all_products(self, info):
        return Product.objects.all()
    all_orders = graphene.List(OrderType)
    def resolve_all_orders(self, info):
        return Order.objects.all()

# Add this if you haven't yet
# schema = graphene.Schema(query=Query)
