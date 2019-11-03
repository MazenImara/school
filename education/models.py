from django.db import models
from user.models import User


# Create your models here.


class Status(models.Model):
	name = models.CharField(max_length=255)
	value = models.CharField(max_length=255)
	color = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Task(models.Model):
	name = models.CharField(max_length=255)
	value = models.CharField(max_length=255)
	order = models.IntegerField()
	description = models.TextField("Description", null=True, blank=True)
	related_tasks = models.ManyToManyField('self', related_name='educations')

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=255)
	value = models.CharField(max_length=255)
	description = models.TextField("Description", null=True, blank=True)

	def __str__(self):
		return self.name


class Education(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField("Description", null=True, blank=True)
	start_at = models.DateTimeField(null=True, blank=True)
	end_at = models.DateTimeField(null=True, blank=True)
	status = models.ForeignKey(Status, on_delete=models.CASCADE, default=Status.objects.get_or_create(value='new')[0].id)
	users = models.ManyToManyField(User, related_name='educations')
	created_at = models.DateTimeField(auto_now_add=True)
	deleted_at = models.DateTimeField(null=True, blank=True)
	tasks = models.ManyToManyField(Task, related_name='educations', through='TaskMemberShip')
	category = models.ForeignKey(Category, related_name='educations', on_delete=models.CASCADE)

	def updateStatus(self, statusId):
		self.status = Status.objects.get(pk=statusId)
		self.save()

	def __str__(self):
		return self.title

	def setData(self, data):
		for key, value in data.items():
			setattr(self, key, value)

	def graphql_update(self, data):
		self.setData(data)
		self.save()
		return self

	def graphql_create(self, data, user):
		self.setData(data)
		self.save()
		self.users.add(user)
		return self

class TaskMemberShip(models.Model):
	education = models.ForeignKey(Education, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE)
	done_at = models.DateTimeField(null=True, blank=True)

