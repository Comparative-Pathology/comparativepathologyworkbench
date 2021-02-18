from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps


"""
    Is there a Cell for a particular Image?
"""
def get_cells_for_image(a_image):

    Cell = apps.get_model('matrices', 'Cell')

    return Cell.objects.filter(image=a_image)

