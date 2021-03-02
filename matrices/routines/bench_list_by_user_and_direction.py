from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps

from django.db.models import Q


"""
    Get All Benches for a particular User
"""
def bench_list_by_user_and_direction(a_user, a_direction):

    MatrixSummary = apps.get_model('matrices', 'MatrixSummary')

    sort_parameter = 'matrix_id'

    if a_direction == '':

        sort_parameter = 'matrix_id'

    else:

        sort_parameter = a_direction

    if a_user.is_superuser:

        queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).order_by(sort_parameter)

    else:

        queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).order_by(sort_parameter)

    return queryset
