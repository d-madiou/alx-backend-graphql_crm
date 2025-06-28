# alx_backend_graphql_crm/schema.py

import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

schema = graphene.Schema(query=Query)
class Query(CRMQuery, graphene.ObjectType):
    pass
class Mutation(CRMMutation, graphene.ObjectType):
    """
    This class combines all mutations from the CRM application.
    It allows for the creation of customers, products, and orders.
    """
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)