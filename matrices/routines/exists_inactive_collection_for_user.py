from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps


"""
    Is there an Inactive Collection for a particular User?
"""
def exists_inactive_collection_for_user(a_user):

    Collection = apps.get_model('matrices', 'Collection')

    return Collection.objects.filter(owner=a_user).filter(active=False).exists()

