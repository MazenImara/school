import graphene
from graphene import ObjectType, Node, Schema, Int
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType

from django.contrib.auth.models import User
from course.models import Course
from status.models import Status

################### Nodes #####################
class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node,)
    pk = Int()
    def resolve_pk(self, info):
        return self.pk


class CourseNode(DjangoObjectType):
    class Meta:
        model = Course
        interfaces = (Node,)
    pk = Int()
    def resolve_pk(self, info):
        return self.pk

class StatusNode(DjangoObjectType):
    class Meta:
        model = Status
        interfaces = (Node,)
    pk = Int()
    def resolve_pk(self, info):
        return self.pk





################### Query #####################
class Query(ObjectType):
    users = DjangoConnectionField(UserNode)
    user = graphene.Field(UserNode, pk=Int())
    def resolve_user(self, info, **kwargs):
        pk = kwargs.get('pk')
        return User.objects.get(pk=pk)

    courses = DjangoConnectionField(CourseNode)
    course = graphene.Field(CourseNode, pk=Int())
    def resolve_course(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Course.objects.get(pk=pk)

    statuses = DjangoConnectionField(StatusNode)
    status = graphene.Field(StatusNode, pk=Int())
    def resolve_status(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Status.objects.get(pk=pk)

schema = Schema(query=Query)