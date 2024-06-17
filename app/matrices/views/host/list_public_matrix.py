#!/usr/bin/python3
###!
# \file         list_public_matrix.py
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
#
# The list_public_matrix VIEW
#
###
from __future__ import unicode_literals

from django import forms

from sortable_listview import SortableListView

from matrices.models import MatrixPublicSummary

from matrices.forms import MatrixPublicSummarySearchForm

from matrices.routines import get_header_data
from matrices.routines import bench_public_list_by_direction
from matrices.routines import get_primary_cpw_environment


#
#   The list_public_matrix VIEW
#
class MatrixPublicListView(SortableListView):

    query_title = forms.CharField(max_length=25)
    query_description = forms.CharField(max_length=25)

    query_search = forms.CharField(max_length=25)

    query_paginate_by = forms.CharField(max_length=12)

    allowed_sort_fields = {'matrix_public_id': {'default_direction': '',
                                                'verbose_name': 'Bench Id'},
                           'matrix_public_title': {'default_direction': '',
                                                   'verbose_name': 'Title'}
                           }

    default_sort_field = 'matrix_public_id'

    paginate_by = 10

    template_name = 'host/list_public_benches.html'

    model = MatrixPublicSummary

    context_object_name = 'matrix_public_summary_list'

    def get_queryset(self):

        if self.request.GET.get('search', None) is None:

            self.query_search = ''

            self.query_title = \
                self.request.GET.get('title', '')
            self.query_description = \
                self.request.GET.get('description', '')

        else:

            self.query_search = self.request.GET.get('search', '')

            self.query_title = ''
            self.query_description = ''

        sort_parameter = ''

        if self.request.GET.get('sort', None) is None:

            sort_parameter = 'matrix_public_id'

        else:

            sort_parameter = self.request.GET.get('sort', None)

        self.query_paginate_by = self.request.GET.get('paginate_by', '')

        if self.query_paginate_by == '':

            self.query_paginate_by = self.paginate_by

        return bench_public_list_by_direction(sort_parameter,
                                              self.query_title,
                                              self.query_description,
                                              '',
                                              '',
                                              '',
                                              '',
                                              '',
                                              self.query_search)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        data = get_header_data(self.request.user)

        data_dict = {'title': self.query_title,
                     'description': self.query_description,
                     'paginate_by': self.query_paginate_by}

        form = MatrixPublicSummarySearchForm(data_dict)

        environment = get_primary_cpw_environment()

        data.update({'form': form,
                     'date_format': environment.date_format})

        context.update(data)

        return context

    def get_paginate_by(self, queryset):

        return self.request.GET.get("paginate_by", self.paginate_by)
