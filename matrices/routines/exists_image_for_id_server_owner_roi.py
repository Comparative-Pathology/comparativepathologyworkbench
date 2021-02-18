from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.db.models import Q 

from django.apps import apps


"""
    Is there an Image for a particular Identifier, Server, Owner and ROI?
"""
def exists_image_for_id_server_owner_roi(a_id, a_server, a_owner, a_roi):

    Image = apps.get_model('matrices', 'Image')
    
    return Image.objects.filter(Q(identifier=a_id) & Q(server=a_server) & Q(owner=a_owner) & Q(roi=a_roi)).exists()


