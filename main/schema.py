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

class PermissionNode(DjangoObjectType):
    class Meta:
        model = Permission
    pk = Int()

class GroupNode(DjangoObjectType):
    class Meta:
        model = Group
    pk = Int()
    permissins = PermissionNode

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node,)
    pk = Int()
    groups = GroupNode()
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
    ### Courses ###
    users = DjangoConnectionField(UserNode)
    @login_required
    def resolve_courses(self, info, **kwargs):
        return self

    user = graphene.Field(UserNode, pk=Int())
    @login_required
    def resolve_user(self, info, **kwargs):
        pk = kwargs.get('pk')
        return User.objects.get(pk=pk)

    logedUser = graphene.Field(UserNode)
    @login_required
    def resolve_logedUser(self, info, **kwargs):
        return info.context.user

    ### Courses ###
    courses = DjangoConnectionField(CourseNode)
    @login_required
    def resolve_courses(self, info, **kwargs):
        return self

    course = graphene.Field(CourseNode, pk=Int())
    def resolve_course(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Course.objects.get(pk=pk)

    statuses = DjangoConnectionField(StatusNode)
    status = graphene.Field(StatusNode, pk=Int())

    def resolve_status(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Status.objects.get(pk=pk)


################### Mutation #####################

class Mutation(ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = Schema(query=Query, mutation=Mutation)
