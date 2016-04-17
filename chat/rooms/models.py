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


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return "[{timestamp}] {handle}: {message}".format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime("%b %-d %-I:%M %p")

    def as_dict(self):
        return {'handle': self.handle,
                'message': self.message,
                'timestamp': self.formatted_timestamp}


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(upload_to=user_directory_path)


class Profile(models.Model):
    """
    The Profile model is used to store extra information about the user
    that doesnt fit into the normal
    """
    #: a one to one relation of profile <> django.contrib.user
    owner = models.OneToOneField(User, related_name='profile')
    avatar_image = models.ImageField(
            upload_to=user_directory_path, blank=True)

    @property
    def avatar_url(self):
        file_name = 'default_avatar.png'
        if self.avatar_image:
            file_name = re.split('/', self.avatar_image.url)[-1]
        #fix this!
        return settings.AVATAR_IMG_URL + file_name

