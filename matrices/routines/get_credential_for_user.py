from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps


"""
    Return the Credential for a particular User
"""
def get_credential_for_user(a_user):

    Credential = apps.get_model('matrices', 'Credential')
    
    return Credential.objects.get(username=a_user.username)
