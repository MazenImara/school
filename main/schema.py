from course.models import Course
from status.models import Status
from graphene import ObjectType, Node, Schema
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType

class CourseNode(DjangoObjectType):

    class Meta:
        model = Course
        interfaces = (Node, )

class StatusNode(DjangoObjectType):

    class Meta:
        model = Status
        interfaces = (Node, )

class Query(ObjectType):
    course = Node.Field(CourseNode)
    all_courses = DjangoConnectionField(CourseNode)

    status = Node.Field(StatusNode)
    all_statuses = DjangoConnectionField(StatusNode)

schema = Schema(query=Query)