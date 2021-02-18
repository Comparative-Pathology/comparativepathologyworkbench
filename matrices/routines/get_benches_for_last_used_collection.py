from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps


"""
    Get the Benches that have last used a particular Collection
"""
def get_benches_for_last_used_collection(a_collection):

    Matrix = apps.get_model('matrices', 'Matrix')

    return Matrix.objects.filter(last_used_collection=a_collection)

