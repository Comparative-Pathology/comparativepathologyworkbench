#!/usr/bin/python3
###!
# \file         views_list_collection.py
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
# The Collection List View
#
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin

from sortable_listview import SortableListView

from matrices.models import CollectionSummary
from matrices.forms import CollectionSummarySearchForm

from matrices.routines import get_header_data
from matrices.routines import collection_list_by_user_and_direction


class CollectionListView(LoginRequiredMixin, SortableListView):

    query_title = forms.CharField(max_length=25)
    query_description = forms.CharField(max_length=25)
    query_owner = forms.CharField(max_length=10)
    query_authority = forms.CharField(max_length=12)
    query_paginate_by = forms.CharField(max_length=12)

    allowed_sort_fields = {'collection_id': {'default_direction': '', 'verbose_name': 'Collection Id'},
                           'collection_title': {'default_direction': '', 'verbose_name': 'Title'},
                           'collection_active': {'default_direction': '', 'verbose_name': 'Activity'},
                           'collection_image_count': {'default_direction': '', 'verbose_name': 'Images'},
                           'collection_owner': {'default_direction': '', 'verbose_name': 'Owner'},
                           'collection_authorisation_authority': {'default_direction': '', 'verbose_name': 'Authority'}
                           }

    default_sort_field = 'collection_id'

    paginate_by = 10

    template_name = 'host/list_collections.html'

    model = CollectionSummary

    context_object_name = 'collection_summary_list'


    def get_queryset(self):

        sort_parameter = ''

        if self.request.GET.get('sort', None) == None:

            sort_parameter = 'collection_id'

        else:

            sort_parameter = self.request.GET.get('sort', None)

        self.query_title = self.request.GET.get('title', '')
        self.query_description = self.request.GET.get('description', '')
        self.query_owner = self.request.GET.get('owner', '')
        self.query_authority = self.request.GET.get('authority', '')
        self.query_paginate_by = self.request.GET.get('paginate_by', '')

        return collection_list_by_user_and_direction(self.request.user, sort_parameter, self.query_title, self.query_description, self.query_owner, self.query_authority)


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        data = get_header_data(self.request.user)

        data_dict = {'title': self.query_title, 'description': self.query_description, 'owner': self.query_owner, 'authority': self.query_authority, 'paginate_by': self.query_paginate_by }

        form = CollectionSummarySearchForm(data_dict)

        data.update({ 'form': form,  })

        context.update(data)

        return context


    def get_paginate_by(self, queryset):

        return self.request.GET.get("paginate_by", self.paginate_by)
