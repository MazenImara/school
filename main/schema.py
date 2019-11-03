import graphene
from graphene import ObjectType
from user.schema import UserQuery, UserMutation
from education.schema import EducationQuery, EducationMutation


################### Nodes #####################




################### Query #####################
class Query(UserQuery, EducationQuery, ObjectType):
    pass


################### Mutation #####################
class Mutation(UserMutation, EducationMutation, ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
