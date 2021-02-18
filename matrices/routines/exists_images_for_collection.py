from __future__ import unicode_literals

import base64, hashlib

from os import urandom


"""
    Get the Images from a particular Collection
"""
def exists_images_for_collection(a_collection):

    images = a_collection.images.all()

    images_exist = True
    
    if not images:
    
        images_exist = False

    
    return images_exist


