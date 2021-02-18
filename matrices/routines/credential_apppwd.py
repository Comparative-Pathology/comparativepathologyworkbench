from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps


"""
    Get the Application Password for a particular User
"""
def credential_apppwd(a_user):

    Credential = apps.get_model('matrices', 'Credential')

    return Credential.objects.filter(username=a_user.username).values('apppwd')

