from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps

from decouple import config


"""
    Get the Primary Wordpress Server - This is the Blogging Engine (Back-end)
"""
def get_primary_wordpress_server():

    Server = apps.get_model('matrices', 'Server')

    return Server.objects.get(url_server=config('WORDPRESS'))

