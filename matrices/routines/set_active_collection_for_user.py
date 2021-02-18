from __future__ import unicode_literals

import base64, hashlib

from os import urandom


from . import get_inactive_collection_for_user


"""
    Set the Active Collection(s) for a particular User to Inactive
"""
def set_active_collection_for_user(a_user):

    collection_list = get_inactive_collection_for_user(a_user)
    
    for collection in collection_list:
    
        collection.set_active()
        
        collection.save()

