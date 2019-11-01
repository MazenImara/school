import graphene
from graphene import ObjectType, Node, Schema, Int
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required

from django.contrib.auth.models import User, Group, Permission
from course.models import Course
from status.models import Status


################### Nodes #####################

class StatusNode(DjangoObjectType):
    class Meta:
        model = Status
        interfaces = (Node,)
    pk = Int()
    def resolve_pk(self, info):
        return self.pk


################### Query #####################
class StatusQuery(ObjectType):

    statuses = DjangoConnectionField(StatusNode)
    status = graphene.Field(StatusNode, pk=Int())

    def resolve_status(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Status.objects.get(pk=pk)


################### Mutation #####################


class StatusMutation(ObjectType):
    pass

