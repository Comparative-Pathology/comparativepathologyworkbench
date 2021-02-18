from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps


"""
    Does a particular User have any Credentials?
"""
def credential_exists(a_user):

    Credential = apps.get_model('matrices', 'Credential')

    return Credential.objects.filter(username=a_user.username).values('username').exists()

