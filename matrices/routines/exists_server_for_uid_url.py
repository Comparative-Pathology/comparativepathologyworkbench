from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.db.models import Q 

from django.apps import apps


"""
    Is there an Image for a particular Identifier, Server, Owner and ROI?
"""
def exists_server_for_uid_url(a_uid, a_url):

    Server = apps.get_model('matrices', 'Server')
    
    return Server.objects.filter(Q(uid=a_uid) & Q(url_server=a_url)).exists()
    


