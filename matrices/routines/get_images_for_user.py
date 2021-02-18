from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps


"""
    Get Active Images for a particular User?
"""
def get_images_for_user(a_user):

    Image = apps.get_model('matrices', 'Image')

    return Image.objects.filter(owner=a_user)

