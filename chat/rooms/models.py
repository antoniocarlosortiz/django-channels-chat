from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)
