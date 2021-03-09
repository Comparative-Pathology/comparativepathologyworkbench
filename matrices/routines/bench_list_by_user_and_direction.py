from __future__ import unicode_literals

import base64, hashlib
import datetime

from os import urandom

from django.contrib.auth.models import User

from django.apps import apps

from django.db.models import Q


"""
    Get All Benches for a particular User
"""
def bench_list_by_user_and_direction(a_user, a_direction, a_query_title, a_query_description, a_query_owner, a_query_authority, a_query_created_after, a_query_created_before, a_query_modified_after, a_query_modified_before, a_query_search_term):

    MatrixSummary = apps.get_model('matrices', 'MatrixSummary')
    Authority = apps.get_model('matrices', 'Authority')

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

    queryset = []

    if a_user.is_superuser:

        if a_query_search_term == '':

            if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after == '' and a_query_modified_before == '':

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

                if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after == '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after != '' and a_query_modified_before == '':
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after != '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after == '' and a_query_modified_before == '':
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_created__lte=date_created_before).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after == '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after != '' and a_query_modified_before == '':
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after != '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after == '' and a_query_modified_before == '':
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after == '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after != '' and a_query_modified_before == '':
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after != '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after == '' and a_query_modified_before == '':
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_created__lte=date_created_before).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after == '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after != '' and a_query_modified_before == '':
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after != '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN')).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

        else:

            queryset = MatrixSummary.objects.filter(Q(matrix_authorisation_authority='ADMIN') & (Q(matrix_title__contains=a_query_search_term) | Q(matrix_description__contains=a_query_search_term)) | Q(matrix_owner__contains=a_query_search_term) | Q(matrix_authorisation_authority__contains=a_query_search_term)).order_by(sort_parameter)

    else:

        if a_query_search_term == '':

            if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after == '' and a_query_modified_before == '':

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

            else:

                if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after == '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after != '' and a_query_modified_before == '':
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before == '' and a_query_modified_after != '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after == '' and a_query_modified_before == '':
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_created__lte=date_created_before).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after == '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after != '' and a_query_modified_before == '':
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter)

                if a_query_created_after == '' and a_query_created_before != '' and a_query_modified_after != '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after == '' and a_query_modified_before == '':
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after == '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after != '' and a_query_modified_before == '':
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before == '' and a_query_modified_after != '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after == '' and a_query_modified_before == '':
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_created__lte=date_created_before).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after == '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after != '' and a_query_modified_before == '':
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

                if a_query_created_after != '' and a_query_created_before != '' and a_query_modified_after != '' and a_query_modified_before != '':
                    date_modified_before = datetime.datetime.strptime(a_query_modified_before, '%d/%m/%Y %H:%M')
                    date_modified_after = datetime.datetime.strptime(a_query_modified_after, '%d/%m/%Y %H:%M')
                    date_created_before = datetime.datetime.strptime(a_query_created_before, '%d/%m/%Y %H:%M')
                    date_created_after = datetime.datetime.strptime(a_query_created_after, '%d/%m/%Y %H:%M')
                    queryset = MatrixSummary.objects.filter(~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)).filter(matrix_modified__lte=date_modified_before).order_by(sort_parameter).filter(matrix_modified__gte=date_modified_after).order_by(sort_parameter).filter(matrix_created__lte=date_created_before).order_by(sort_parameter).filter(matrix_created__gte=date_created_after).order_by(sort_parameter)

        else:

            queryset = MatrixSummary.objects.filter((~Q(matrix_authorisation_authority='ADMIN') & Q(matrix_authorisation_permitted=a_user.username)) & (Q(matrix_title__contains=a_query_search_term) | Q(matrix_description__contains=a_query_search_term)) | Q(matrix_owner__contains=a_query_search_term) | Q(matrix_authorisation_authority__contains=a_query_search_term)).order_by(sort_parameter)


    return queryset
