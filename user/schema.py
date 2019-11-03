import graphene
from graphene import ObjectType, Node, Schema, Int, String, Boolean, Mutation, InputObjectType, Field
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required

from django.contrib.auth.models import Group, Permission
from user.models import User


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
    def resolve_pk(self, info):
        return self.pk



################### Query #####################
class UserQuery(ObjectType):
    ### User ###
    users = DjangoConnectionField(UserNode)

    user = graphene.Field(UserNode, pk=Int())
    @login_required
    def resolve_user(self, info, **kwargs):
        pk = kwargs.get('pk')
        return User.objects.get(pk=pk)

    logedUser = graphene.Field(UserNode)
    @login_required
    def resolve_logedUser(self, info, **kwargs):
        return info.context.user


################### Mutation #####################

class UserInput(InputObjectType):
        pk = Int()
        email = String()
        password = String()
        first_name = String()
        last_name = String()
        address = String()
        zip_code = String()
        city = String()
        phone = String()

class CreateOrUpdateAdminUser(Mutation):
    errors = String()
    success = Boolean()
    user = Field(UserNode)

    class Arguments:
        input = UserInput()

    def mutate(self, info, input=None):
        if input.pk:
            user = User.objects.get(pk=input.pk).graphql_update(input)
        else:
            user = User().graphql_create(input, 'admin')

        return CreateOrUpdateAdminUser(
            success = True,
            user = user
        )


class CreateOrUpdateEducatorUser(Mutation):
    errors = String()
    success = Boolean()
    user = Field(UserNode)

    class Arguments:
        input = UserInput()

    def mutate(self, info, input=None):
        if input.pk:
            user = User.objects.get(pk=input.pk).graphql_update(input)
        else:
            user = User().graphql_create(input, 'educator')

        return CreateOrUpdateAdminUser(
            success = True,
            user = user
        )


class CreateOrUpdateVendorUser(Mutation):
    errors = String()
    success = Boolean()
    user = Field(UserNode)

    class Arguments:
        input = UserInput()

    def mutate(self, info, input=None):
        if input.pk:
            user = User.objects.get(pk=input.pk).graphql_update(input)
        else:
            user = User().graphql_create(input, 'vendor')

        return CreateOrUpdateAdminUser(
            success = True,
            user = user
        )

class UserMutation(ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    CreateOrUpdateAdminUser = CreateOrUpdateAdminUser.Field()
    CreateOrUpdateEducatorUser = CreateOrUpdateEducatorUser.Field()
    CreateOrUpdateVendorUser = CreateOrUpdateVendorUser.Field()

