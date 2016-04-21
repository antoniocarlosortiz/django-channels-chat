import requests

from django.core.files.base import ContentFile

from rooms.models import Profile


def get_facebook_avatar(strategy, user, response, details,
                        is_new, *args, **kwargs):
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(owner=user)

    if profile.avatar_image:
        return

    if "facebook" in kwargs['backend'].redirect_uri:
        image_url = 'http://graph.facebook.com/%s/picture?type=large' % \
            kwargs['uid']
        avatar = requests.get(image_url).content
        profile.avatar_image.save('{0}.jpeg'.format(user.pk),
                                  ContentFile(avatar))

        profile.save()
