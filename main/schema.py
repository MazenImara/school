import graphene
from graphene import ObjectType
from user.schema import UserQuery, UserMutation
from course.schema import CourseQuery, CourseMutation
from status.schema import StatusQuery, StatusMutation


################### Nodes #####################




################### Query #####################
class Query(UserQuery, CourseQuery, StatusQuery, ObjectType):
    pass


################### Mutation #####################
class Mutation(UserMutation, ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
