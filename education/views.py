from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from education.models import Category, Education
from user.models import User




def index(request):
    education = Education()
    category = Category.objects.get(pk=1)
    education.category = category
    education.title = 'input.title'
    education.description = 'input.description'
    education.save()
    return HttpResponse(education.category.name)
