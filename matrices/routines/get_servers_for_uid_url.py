from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.db.models import Q 

from django.apps import apps


"""
    Get the Images from a particular Collection
"""
def get_servers_for_uid_url(a_uid, a_url):

    Server = apps.get_model('matrices', 'Server')
    
    return Server.objects.get(Q(uid=a_uid) & Q(url_server=a_url))
