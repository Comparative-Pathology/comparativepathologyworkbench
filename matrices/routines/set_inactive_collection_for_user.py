from __future__ import unicode_literals

import base64, hashlib

from os import urandom


from . import get_active_collection_for_user


"""
    Set the Inactive Collection(s) for a particular User to Inactive
"""
def set_inactive_collection_for_user(a_user):

    collection_list = get_active_collection_for_user(a_user)
    
    for collection in collection_list:
    
        collection.set_inactive()
        
        collection.save()
    
