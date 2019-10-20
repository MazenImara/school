from django.db import models

# Create your models here.

class Status(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.name
