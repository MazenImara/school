import graphene
from graphene import ObjectType, Node, Schema, Int, Mutation, String
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required

from course.models import Course


################### Nodes #####################
class CourseNode(DjangoObjectType):
    class Meta:
        model = Course
        interfaces = (Node,)
    pk = Int()
    def resolve_pk(self, info):
        return self.pk


################### Query #####################
class CourseQuery(ObjectType):

    ### Courses ###
    courses = DjangoConnectionField(CourseNode)
    @login_required
    def resolve_courses(self, info, **kwargs):
        return self

    course = graphene.Field(CourseNode, pk=Int())
    def resolve_course(self, info, **kwargs):
        pk = kwargs.get('pk')
        return Course.objects.get(pk=pk)


################### Mutation #####################

class UpdateCourseStatus(Mutation):
    success = String()

    class Arguments:
        statusId = Int()
        courseId = Int()

    def mutate(self, info, statusId, courseId):
        course = Course.objects.get(pk=courseId)
        course.updateStatus(statusId)
        return UpdateCourseStatus(
            success = "True",
        )


class CourseMutation(ObjectType):
    updateCourseStatus = UpdateCourseStatus.Field()

