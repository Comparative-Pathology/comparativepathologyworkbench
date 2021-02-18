from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps

from . import get_active_collection_for_user


"""
    Get the Active Collection(s) for a particular User
"""
def get_active_collection_images_for_user(a_user):

    collection_list = get_active_collection_for_user(a_user)
    
    active_collection = collection_list[0]
        
    return active_collection.images.all()

