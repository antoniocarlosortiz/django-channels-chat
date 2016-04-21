from __future__ import unicode_literals

import re
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured


class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return self.label


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)


class Profile(models.Model):
    """
    The Profile model is used to store extra information about the user
    that doesnt fit into the normal
    """
    #: a one to one relation of profile <> django.contrib.user
    owner = models.OneToOneField(User, related_name='profile')
    avatar_image = models.ImageField(
            upload_to=user_directory_path, blank=True)


class Message(models.Model):
    owner = models.ForeignKey(Profile, related_name='messages')
    room = models.ForeignKey(Room, related_name='messages')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return "[{timestamp}] {owner}: {message}".format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime("%b %-d %-I:%M %p")

    def as_dict(self):
        return {'avatar_image_url': self.owner.avatar_image.url,
                'message': self.message,
                'timestamp': self.formatted_timestamp}



