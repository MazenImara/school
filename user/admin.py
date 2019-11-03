from django.contrib import admin
from .models import *


# Register your models here.
class UserAdmin(admin.ModelAdmin):
	empty_value_display = '-empty-'


admin.site.register(User, UserAdmin)
