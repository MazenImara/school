from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
from django.contrib.auth.models import Group


class User(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(max_length=30, null=True, blank=True)
	last_name = models.CharField(max_length=30, null=True, blank=True)
	email = models.EmailField(unique=True)
	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
		help_text=_('Designates whether the user can log into this admin site.'),
	)
	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. ''Unselect this instead of deleting accounts.'
		),
	)

	address = models.TextField("Address", null=True, blank=True)

	zip_code = models.CharField(
		"ZIP / Postal code",
		max_length=12,
		null=True, blank=True
	)

	city = models.TextField("City", null=True, blank=True)

	phone = PhoneNumberField(null=True, blank=True, unique=True)



	USERNAME_FIELD = 'email'
	objects = UserManager()

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def get_full_name(self):
		return '%s %s' % (self.first_name, self.last_name)

	def get_short_name(self):
		return self.get_full_name()

	def __str__(self):
		return self.get_full_name()

	def create_educator(self, email, password):
		return self.create_set_group(email, password, 'educator')

	def create_admin(self, email, password):
		return self.create_set_group(email, password, 'admin')

	def create_vendor(self, email, password):
		return self.create_set_group(email, password, 'vendor')

	def create_set_group(self, email, password, group_name):
		self.email = email
		self.set_password(password)
		self.save()
		return self.add_group(group_name)

	def create_set_group_id(self, email, password, group_id):
		self.email = email
		self.set_password(password)
		self.save()
		self.groups.add(Group.objects.get(pk=group_id))
		return self

	def add_group(self, name):
		group, created = Group.objects.get_or_create(name=name)
		self.groups.add(group)
		return self

	def setData(self, data):
		for key, value in data.items():
			setattr(self, key, value)

	def update(self, data):
		self.setData(data)
		self.save()
		return self

	def create(self, group_name, data):
		self.setData(data)
		self.save()
		return self.add_group(group_name)



