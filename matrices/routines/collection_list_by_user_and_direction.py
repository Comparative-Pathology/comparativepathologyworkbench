from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps

from django.db.models import Q


"""
    Get All Collections for a particular User
"""
def collection_list_by_user_and_direction(a_user, a_direction):

    CollectionSummary = apps.get_model('matrices', 'CollectionSummary')

    sort_parameter = 'collection_id'

    if a_direction == '':

        sort_parameter = 'collection_id'

    else:

        sort_parameter = a_direction


    if a_user.is_superuser:

        queryset = CollectionSummary.objects.filter(Q(collection_authorisation_authority='ADMIN')).order_by(sort_parameter)

    else:

        queryset = CollectionSummary.objects.filter(~Q(collection_authorisation_authority='ADMIN') & Q(collection_authorisation_permitted=a_user.username)).order_by(sort_parameter)

    return queryset
