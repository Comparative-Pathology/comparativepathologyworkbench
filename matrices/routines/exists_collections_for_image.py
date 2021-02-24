from __future__ import unicode_literals

import base64, hashlib

from os import urandom


"""
    Get All Collections for an Image
"""
def exists_collections_for_image(a_image):

    collections = a_image.collections.all()
    
    collections_exist = True
    
    if not collections:
    
        collections_exist = False

    return collections_exist

