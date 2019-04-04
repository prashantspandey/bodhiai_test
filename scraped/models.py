from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class JobAlert(models.Model):
    title = models.CharField(max_length = 200)
    date = models.DateField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return str(self.title)

