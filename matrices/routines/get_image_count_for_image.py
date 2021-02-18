from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps


"""
    Count the Images for a particular Image
"""
def get_image_count_for_image(image_id):

    Image = apps.get_model('matrices', 'Image')

    return Image.objects.filter(identifier=image_id).count()

