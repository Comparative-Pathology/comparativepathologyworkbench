from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.contrib.auth.models import User

from django.apps import apps

from django.db.models import Q


"""
    Get All Benches for a particular User
"""
def bench_list_by_user_and_direction(a_user, a_direction, a_query_title, a_query_description, a_query_owner, a_query_authority, a_query_created_after, a_query_created_before, a_query_modified_after, a_query_modified_before):

    MatrixSummary = apps.get_model('matrices', 'MatrixSummary')
    Authority = apps.get_model('matrices', 'Authority')

    #print("a_query_title : " + str(a_query_title))
    #print("a_query_description : " + str(a_query_description))
    #print("a_query_created_after : " + str(a_query_created_after))
    #print("a_query_created_before : " + str(a_query_created_before))
    #print("a_query_modified_after : " + str(a_query_modified_after))
    #print("a_query_modified_before : " + str(a_query_modified_before))
    #print("a_query_owner : " + str(a_query_owner))
    #print("a_query_authority : " + str(a_query_authority))

    str_query_authority = ''
    str_query_owner = ''

    if a_query_description != '':
        a_query_description = a_query_description

    if a_query_authority != '':

        authority = Authority.objects.get(pk=int(a_query_authority))
        str_query_authority = authority.name

    if a_query_owner != '':

        user = User.objects.get(pk=int(a_query_owner))
        str_query_owner = user.username

    sort_parameter = 'matrix_id'

    if a_direction == '':

        sort_parameter = 'matrix_id'

    else:

        sort_parameter = a_direction

    if a_user.is_superuser:

        if a_query_title == '' and a_query_description == '' and str_query_owner == '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner == '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner != '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner != '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_owner=str_query_owner).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner == '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_description__contains=a_query_description)).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner == '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_description__contains=a_query_description)).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner != '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_description__contains=a_query_description)).filter(matrix_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner != '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_description__contains=a_query_description)).filter(matrix_owner=str_query_owner).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner == '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_title__contains=a_query_title)).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner == '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_title__contains=a_query_title)).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner != '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_title__contains=a_query_title)).filter(matrix_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner != '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_title__contains=a_query_title)).filter(matrix_owner=str_query_owner).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner == '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_title__contains=a_query_title) & Q(matrix_description__contains=a_query_description)).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner == '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_title__contains=a_query_title) & Q(matrix_description__contains=a_query_description)).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner != '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_title__contains=a_query_title) & Q(matrix_description__contains=a_query_description)).filter(matrix_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner != '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & Q(matrix_title__contains=a_query_title) & Q(matrix_description__contains=a_query_description)).filter(matrix_owner=str_query_owner).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

    else:

        if a_query_title == '' and a_query_description == '' and str_query_owner == '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner == '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner != '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title == '' and a_query_description == '' and str_query_owner != '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_owner=str_query_owner).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner == '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_description__contains=a_query_description)).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner == '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_description__contains=a_query_description)).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner != '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_description__contains=a_query_description)).filter(matrix_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title == '' and a_query_description != '' and str_query_owner != '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_description__contains=a_query_description)).filter(matrix_owner=str_query_owner).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner == '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_title__contains=a_query_title)).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner == '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_title__contains=a_query_title)).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner != '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_title__contains=a_query_title)).filter(matrix_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title != '' and a_query_description == '' and str_query_owner != '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_title__contains=a_query_title)).filter(matrix_owner=str_query_owner).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner == '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_title__contains=a_query_title) & Q(matrix_description__contains=a_query_description)).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner == '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_title__contains=a_query_title) & Q(matrix_description__contains=a_query_description)).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner != '' and str_query_authority == '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_title__contains=a_query_title) & Q(matrix_description__contains=a_query_description)).filter(matrix_owner=str_query_owner).order_by(sort_parameter)

        if a_query_title != '' and a_query_description != '' and str_query_owner != '' and str_query_authority != '':
            queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username) & Q(matrix_title__contains=a_query_title) & Q(matrix_description__contains=a_query_description)).filter(matrix_owner=str_query_owner).filter(matrix_authorisation_authority=str_query_authority).order_by(sort_parameter)

    return queryset
