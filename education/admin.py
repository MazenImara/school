from django.contrib import admin
from .models import *


# Register your models here.
class EducationAdmin(admin.ModelAdmin):
	empty_value_display = '-empty-'


admin.site.register(Education, EducationAdmin)


class StatusAdmin(admin.ModelAdmin):
	empty_value_display = '-empty-'


admin.site.register(Status, StatusAdmin)


class CategoryAdmin(admin.ModelAdmin):
	empty_value_display = '-empty-'


admin.site.register(Category, CategoryAdmin)


class TaskAdmin(admin.ModelAdmin):
	empty_value_display = '-empty-'


admin.site.register(Task, TaskAdmin)
