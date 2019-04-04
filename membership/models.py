from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from basicinformation.models import *

class FirebaseToken(models.Model):
    user = models.ForeignKey(User,null=True,blank=True)
    token = models.CharField(max_length = 500)

    def __str__(self):
        return str(self.user) + ' ' + str(self.token)
 
