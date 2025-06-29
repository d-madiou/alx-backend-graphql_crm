# ALX Backend GraphQL CRM

This is a Customer Relationship Management (CRM) system built with **Django** and **GraphQL** using the `graphene-django` library. It allows creating, retrieving, and filtering customers, products, and orders via a GraphQL API.

## Features

- GraphQL endpoint at `/graphql`
- Mutations:
  - Create single or bulk customers
  - Create products
  - Create orders with associated products
- Queries:
  - List and filter customers, products, and orders
- Filtering using `django-filter`
- Admin panel for managing data manually

## Technologies Used

- Python 3.10+
- Django 4.2+
- Graphene-Django
- Django Filter
- SQLite (default)

## Setup Instructions

1. **Clone the repo**:
   ```bash
   git clone https://github.com/d-madiou/alx-backend-graphql_crm.git
   cd alx-backend-graphql_crm
