from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from education.models import *
from user.models import User




def index(request):
    education = Education.objects.all()[0]
    education.add_tasks()
    return HttpResponse(education.tasks.all())
