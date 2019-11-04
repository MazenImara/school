import json

import graphene
from graphene import ObjectType, Node, Schema, Int, Mutation, String, InputObjectType, Field, Boolean
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required

from education.models import *


################### Nodes #####################
class EducationNode(DjangoObjectType):
    class Meta:
        model = Education
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

class EducationCategoryNode(DjangoObjectType):
    class Meta:
        model = EducationCategory
        interfaces = (Node,)
    pk = Int()
    def resolve_pk(self, info):
        return self.pk

class TaskNode(DjangoObjectType):
    class Meta:
        model = Task
        interfaces = (Node,)
    pk = Int()
    def resolve_pk(self, info):
        return self.pk

################### Query #####################
class EducationQuery(ObjectType):

    ### Educations ###
    educations = DjangoConnectionField(EducationNode)
    @login_required
    def resolve_educations(self, info, **kwargs):
        return self

    education = Field(EducationNode, pk=Int())
    def resolve_education(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Education.objects.get(pk=pk)

    statuses = DjangoConnectionField(StatusNode)
    status = graphene.Field(StatusNode, pk=Int())
    def resolve_status(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Status.objects.get(pk=pk)

    categories = DjangoConnectionField(EducationCategoryNode)

    tasks = DjangoConnectionField(TaskNode)
    task = graphene.Field(TaskNode, pk=Int())
    def resolve_task(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Task.objects.get(pk=pk)

################### Mutation #####################

class UpdateEducationStatus(Mutation):
    success = Boolean()

    class Arguments:
        statusId = Int()
        educationId = Int()

    def mutate(self, info, statusId, educationId):
        education = Education.objects.get(pk=educationId)
        education.updateStatus(statusId)
        return UpdateEducationStatus(
            success = True,
        )

class EducationInput(InputObjectType):
        pk = Int()
        title = String()
        category_id = Int()
        description = String()
        start_at =graphene.types.datetime.DateTime()
        end_at =graphene.types.datetime.DateTime()

class CreateOrUpdateEducation(Mutation):
    errors = String()
    success = Boolean()
    education = Field(EducationNode)

    class Arguments:
        input = EducationInput()

    def mutate(self, info, input=None):
        if input.pk:
            education = Education.objects.get(pk=input.pk).update(input)
        else:
            education = Education().create(info.context.user, input)

        return CreateOrUpdateEducation(
            success = True,
            education = education
        )


class EducationMutation(ObjectType):
    updateEducationStatus = UpdateEducationStatus.Field()
    createOrUpdateEducation = CreateOrUpdateEducation.Field()

