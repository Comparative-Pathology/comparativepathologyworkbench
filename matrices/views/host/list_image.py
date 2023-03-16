#!/usr/bin/python3
###!
# \file         list_image.py
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
# The list_images VIEW
#
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from sortable_listview import SortableListView

from matrices.models import Collection
from matrices.models import ImageSummary

from matrices.forms import ImageSummarySearchForm

from matrices.routines import credential_exists
from matrices.routines import get_images_for_collection
from matrices.routines import get_hidden_images_for_collection
from matrices.routines import get_header_data
from matrices.routines import image_list_by_user_and_direction

#
# The list_images VIEW
#
class ImageListView(LoginRequiredMixin, SortableListView):

    query_name = forms.CharField(max_length=25)
    query_server = forms.CharField(max_length=25)
    query_roi = forms.IntegerField()
    query_comment = forms.CharField(max_length=25)
    query_hidden = forms.BooleanField()
    query_owner = forms.CharField(max_length=25)
    query_collection_id = forms.CharField(max_length=25)
    query_matrix_id = forms.CharField(max_length=25)

    query_search = forms.CharField(max_length=25)

    query_paginate_by = forms.CharField(max_length=12)

    allowed_sort_fields = {'image_name': {'default_direction': '', 'verbose_name': 'Name'},
                           'image_comment': {'default_direction': '', 'verbose_name': 'Comment'},
                           'image_roi': {'default_direction': '', 'verbose_name': 'ROI'},
                           'image_hidden': {'default_direction': '', 'verbose_name': 'Hidden?'},
                           'image_owner': {'default_direction': '', 'verbose_name': 'Owner'},
                           'image_server': {'default_direction': '', 'verbose_name': 'Server'},
                           'image_collection_id': {'default_direction': '', 'verbose_name': 'Collection'},
                           'image_matrix_id': {'default_direction': '', 'verbose_name': 'Bench'}
                           }


    default_sort_field = 'image_name'

    paginate_by = 7

    template_name = 'host/list_images.html'

    model = ImageSummary

    context_object_name = 'image_summary_list'


    def get_queryset(self):

        kwargs_collection_id = ''

        if self.kwargs != None and self.kwargs != {}:
                
            kwargs_collection_id = self.kwargs['collection_id']

        self.query_name = self.request.GET.get('name', '')
        self.query_server = self.request.GET.get('server', '')
        self.query_roi = self.request.GET.get('roi', '')
        self.query_comment = self.request.GET.get('comment', '')
        self.query_hidden = self.request.GET.get('hidden', '')
        self.query_owner = self.request.GET.get('owner', '')
        self.query_collection_id = self.request.GET.get('collection_id', '')

        if kwargs_collection_id != '':
        
            collection_id = kwargs_collection_id
        
        else:

            collection_id = self.query_collection_id

        self.query_bench_id = self.request.GET.get('bench_id', '')

        sort_parameter = ''

        if self.request.GET.get('sort', None) == None:

            sort_parameter = 'image_name'

        else:

            sort_parameter = self.request.GET.get('sort', None)

        self.query_paginate_by = self.request.GET.get('paginate_by', '')

        if self.request.GET.get('hidden', None) == 'on':

            self.query_hidden = True

        else:

            self.query_hidden = False


        return image_list_by_user_and_direction(self.request.user, sort_parameter, self.query_name, self.query_server, self.query_roi, self.query_comment, \
                                        self.query_hidden, self.query_owner, collection_id, self.query_bench_id )


    def get_context_data(self, **kwargs):

        collection_id = ''
        context = super().get_context_data(**kwargs)

        allBoolean = True

        if self.kwargs != None and self.kwargs != {}:
                
            allBoolean = False
            collection_id = self.kwargs['collection_id']

        if collection_id == '' or collection_id == 0 :

            collection_id = self.query_collection_id

        collection = None
        collection_image_list = []
        collection_hidden_image_list = []

        int_collection_id = 0
        if collection_id != '':
            int_collection_id = int(collection_id)

            collection = get_object_or_404(Collection, pk=collection_id)
            collection_image_list = get_images_for_collection(collection)
            collection_hidden_image_list = get_hidden_images_for_collection(collection)

        data = get_header_data(self.request.user)

        readBoolean = False

        if credential_exists(self.request.user):

            readBoolean = True

        data_dict = { 'name': self.query_name, 'server': self.query_server, 'roi': self.query_roi, 'comment': self.query_comment, 'hidden': self.query_hidden, \
                    'owner': self.query_owner, 'collection_id': self.query_collection_id, 'bench_id': self.query_bench_id, 'paginate_by': self.query_paginate_by  }

        form = ImageSummarySearchForm(data_dict, request=self.request)

        data.update({ 'form': form, 'allBoolean': allBoolean, 'readBoolean': readBoolean, 'collection_id': int_collection_id, 'collection': collection, \
                     'collection_image_list': collection_image_list, 'collection_hidden_image_list': collection_hidden_image_list })

        context.update(data)

        return context


    def get_paginate_by(self, queryset):

        return self.request.GET.get("paginate_by", self.paginate_by)
