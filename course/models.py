from django.db import models

# Create your models here.
from status.models import Status


class Course(models.Model):
    title = models.CharField(max_length=255)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.title