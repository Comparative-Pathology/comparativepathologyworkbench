from __future__ import unicode_literals

import base64, hashlib

from os import urandom


from . import exists_inactive_collection_for_user
from . import get_inactive_collection_for_user


"""
    Set the Inactive Collection(s) for a particular User to Active
"""
def set_first_active_collection_for_user(a_user):

    if exists_inactive_collection_for_user(a_user):
    
        collection_list = get_inactive_collection_for_user(a_user)
    
        collection = collection_list[0]
    
        collection.set_active()
        
        collection.save()

