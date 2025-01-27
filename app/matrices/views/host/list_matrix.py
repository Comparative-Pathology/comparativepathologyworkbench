#!/usr/bin/python3
#
# ##
# \file         list_matrix.py
# \author       Mike Wicks
# \date         March 2021
# \version      $Id$
# \par
# (C) University of Edinburgh, Edinburgh, UK
# (C) Heriot-Watt University, Edinburgh, UK
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be
# useful but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
# \brief
# The list_benches VIEW
# ##
#
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin

from matrices.models import Credential
from matrices.models import MatrixSummary

from matrices.forms import MatrixSummarySearchForm

from matrices.routines import get_bench_count_for_user
from matrices.routines import get_header_data
from matrices.routines import bench_list_by_user_and_direction
from matrices.routines import get_primary_cpw_environment

from sortable_listview import SortableListView


#
#   The list_benches VIEW
#
class MatrixListView(LoginRequiredMixin, SortableListView):

    query_title = forms.CharField(max_length=25)
    query_description = forms.CharField(max_length=25)
    query_created_after = forms.DateTimeField()
    query_created_before = forms.DateTimeField()
    query_modified_after = forms.DateTimeField()
    query_modified_before = forms.DateTimeField()
    query_owner = forms.CharField(max_length=10)
    query_authority = forms.CharField(max_length=12)

    query_search = forms.CharField(max_length=25)

    query_paginate_by = forms.CharField(max_length=12)

    allowed_sort_fields = {'matrix_id': {'default_direction': '',
                                         'verbose_name': 'Bench Id'},
                           'matrix_title': {'default_direction': '',
                                            'verbose_name': 'Title'},
                           'matrix_created': {'default_direction': '',
                                              'verbose_name': 'Created On'},
                           'matrix_modified': {'default_direction': '',
                                               'verbose_name': 'Updated On'},
                           'matrix_owner': {'default_direction': '',
                                            'verbose_name': 'Owner'},
                           'matrix_authorisation_authority': {
                                'default_direction': '',
                                'verbose_name': 'Authority'}
                           }

    default_sort_field = 'matrix_id'

    paginate_by = 10

    template_name = 'host/list_benches.html'

    model = MatrixSummary

    context_object_name = 'matrix_summary_list'

    def get_queryset(self):

        if self.request.GET.get('search', None) is None:

            self.query_search = ''

            self.query_title = \
                self.request.GET.get('title', '')
            self.query_description = \
                self.request.GET.get('description', '')
            self.query_owner = \
                self.request.GET.get('owner', '')
            self.query_authority = \
                self.request.GET.get('authority', '')
            self.query_created_before = \
                self.request.GET.get('created_before', '')
            self.query_created_after = \
                self.request.GET.get('created_after', '')
            self.query_modified_before = \
                self.request.GET.get('modified_before', '')
            self.query_modified_after = \
                self.request.GET.get('modified_after', '')

        else:

            self.query_search = self.request.GET.get('search', '')

            self.query_title = ''
            self.query_description = ''
            self.query_owner = ''
            self.query_authority = ''
            self.query_created_before = ''
            self.query_created_after = ''
            self.query_modified_before = ''
            self.query_modified_after = ''

        sort_parameter = ''

        if self.request.GET.get('sort', None) is None:

            sort_parameter = 'matrix_id'

        else:

            sort_parameter = self.request.GET.get('sort', None)

        self.query_paginate_by = self.request.GET.get('paginate_by', '')

        if self.query_paginate_by == '':

            self.query_paginate_by = self.paginate_by

        return bench_list_by_user_and_direction(self.request.user,
                                                sort_parameter,
                                                self.query_title,
                                                self.query_description,
                                                self.query_owner,
                                                self.query_authority,
                                                self.query_created_after,
                                                self.query_created_before,
                                                self.query_modified_after,
                                                self.query_modified_before,
                                                self.query_search)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        data = get_header_data(self.request.user)

        readBoolean = False

        credential = Credential.objects.get_or_none(username=self.request.user.username)

        if credential:

            readBoolean = True

        data_dict = {'title': self.query_title,
                     'description': self.query_description,
                     'created_before': self.query_created_before,
                     'created_after': self.query_created_after,
                     'modified_before': self.query_modified_before,
                     'modified_after': self.query_modified_after,
                     'owner': self.query_owner,
                     'authority': self.query_authority,
                     'paginate_by': self.paginate_by}

        form = MatrixSummarySearchForm(data_dict)

        createBoolean = True

        environment = get_primary_cpw_environment()

        if get_bench_count_for_user(self.request.user) >= \
                environment.maximum_bench_count and \
                self.request.user.username == 'guest':

            createBoolean = False

        data.update({'form': form,
                     'readBoolean': readBoolean,
                     'createBoolean': createBoolean,
                     'date_format': environment.date_format})

        context.update(data)

        return context

    def get_paginate_by(self, queryset):

        return self.request.GET.get("paginate_by", self.query_paginate_by)
