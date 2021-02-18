from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps


"""
    Is there a Collection Authorisation for a particular Collection and a particular User?
"""
def collection_authorisation_exists_for_collection_and_permitted(a_collection, a_user):

    CollectionAuthorisation = apps.get_model('matrices', 'CollectionAuthorisation')

    return CollectionAuthorisation.objects.filter(collection=a_collection).filter(permitted=a_user).exists()

