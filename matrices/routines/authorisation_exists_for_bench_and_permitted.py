from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps


"""
    Is there an Authorisation for a particular Bench and a particular User?
"""
def authorisation_exists_for_bench_and_permitted(a_matrix, a_user):

    Authorisation = apps.get_model('matrices', 'Authorisation')

    return Authorisation.objects.filter(matrix=a_matrix).filter(permitted=a_user).exists()


