from __future__ import unicode_literals

import base64, hashlib

from os import urandom


"""
    Get the Images from a particular Collection
"""
def get_images_for_collection(a_collection):

    return a_collection.images.all()

