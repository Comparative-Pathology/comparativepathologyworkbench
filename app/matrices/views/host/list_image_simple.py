#!/usr/bin/python3
#
# ##
# \file         list_image_simple.py
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
# The list_images_simple VIEW
# ##
#
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin

from matrices.models import Credential
from matrices.models import ImageSummary

from matrices.forms import ImageSummarySimpleSearchForm

from matrices.routines import get_header_data
from matrices.routines import image_list_by_user_and_direction

from sortable_listview import SortableListView


#
#   The list_images VIEW
#
class ImageSimpleListView(LoginRequiredMixin, SortableListView):

    query_name = forms.CharField(max_length=25)
    query_owner = forms.CharField(max_length=25)
    query_sort_field = forms.CharField(max_length=25)
    query_sort_direction = forms.CharField(max_length=25)

    query_search = forms.CharField(max_length=25)

    query_paginate_by = forms.CharField(max_length=12)

    allowed_sort_fields = {
        'image_name': {'default_direction': '', 'verbose_name': 'Name'},
        'image_comment': {'default_direction': '', 'verbose_name': 'Comment'},
        'image_roi': {'default_direction': '', 'verbose_name': 'ROI'},
        'image_hidden': {'default_direction': '', 'verbose_name': 'Hidden?'},
        'image_owner': {'default_direction': '', 'verbose_name': 'Owner'},
        'image_tag_id': {'default_direction': '', 'verbose_name': 'Tag'},
        'image_source': {'default_direction': '', 'verbose_name': 'Source'},
        'image_collection_id': {'default_direction': '', 'verbose_name': 'Collection'},
        'image_matrix_id': {'default_direction': '', 'verbose_name': 'Bench'}
    }

    default_sort_field = 'image_name'

    paginate_by = 10

    template_name = 'host/list_images_simple.html'

    model = ImageSummary

    context_object_name = 'image_summary_list'

    def get_queryset(self):

        sort_parameter = ''
        sort_direction = ''

        # Get the URL GET Parameters
        self.query_name = self.request.GET.get('name', '')
        self.query_sort_field = self.request.GET.get('sort_field', '')
        self.query_sort_direction = self.request.GET.get('sort_direction', '')
        self.query_owner = self.request.GET.get('owner', '')

        # Set the Sort Parameter
        if self.request.GET.get('sort_field', None) is None:

            sort_parameter = 'image_name'

        else:

            sort_parameter = self.request.GET.get('sort_field', None)
            sort_direction = self.request.GET.get('sort_direction', None)

            if sort_direction is None:

                sort_direction = ''

            else:

                if sort_direction == 'ascending':

                    sort_direction = ''

                if sort_direction == 'descending':

                    sort_direction = '-'

            if sort_parameter == 'name':

                sort_parameter = sort_direction + 'image_name'

            if sort_parameter == 'comment':

                sort_parameter = sort_direction + 'image_comment'

            if sort_parameter == 'roi':

                sort_parameter = sort_direction + 'image_roi'

            if sort_parameter == 'hidden':

                sort_parameter = sort_direction + 'image_hidden'

            if sort_parameter == 'owner':

                sort_parameter = sort_direction + 'image_owner'

            if sort_parameter == 'tag':

                sort_parameter = sort_direction + 'image_tag_ids'

            if sort_parameter == 'source':

                sort_parameter = sort_direction + 'image_server_id'

            if sort_parameter == 'collection':

                sort_parameter = sort_direction + 'image_collection_ids'

            if sort_parameter == 'bench':

                sort_parameter = sort_direction + 'image_matrix_ids'

        # Set the Pagination Parameter
        self.query_paginate_by = self.request.GET.get('paginate_by', None)

        images = image_list_by_user_and_direction(self.request.user,
                                                  sort_parameter,
                                                  self.query_name,
                                                  '',
                                                  '',
                                                  '',
                                                  False,
                                                  self.query_owner,
                                                  '',
                                                  '',
                                                  '')

        return images

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        data = get_header_data(self.request.user)

        readBoolean = False

        credential = Credential.objects.get_or_none(username=self.request.user.username)

        if credential:

            readBoolean = True

        data_dict = {'name': self.query_name,
                     'sort_field': self.query_sort_field,
                     'sort_direction': self.query_sort_direction,
                     'owner': self.query_owner,
                     'paginate_by': self.query_paginate_by}

        form = ImageSummarySimpleSearchForm(data_dict, request=self.request)

        data.update({'form': form,
                     'readBoolean': readBoolean})

        context.update(data)

        return context

    def get_paginate_by(self, queryset):

        return self.request.GET.get("paginate_by", self.paginate_by)
