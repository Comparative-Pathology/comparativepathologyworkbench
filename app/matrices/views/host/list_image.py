#!/usr/bin/python3
#
# ##
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
# The list_images VIEW
# ##
#
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin

from matrices.models import Collection
from matrices.models import Credential
from matrices.models import ImageSummary

from matrices.forms import ImageSummarySearchForm

from matrices.routines import get_header_data
from matrices.routines import get_or_none_tag
from matrices.routines import image_list_by_user_and_direction

from sortable_listview import SortableListView


#
#   The list_images VIEW
#
class ImageListView(LoginRequiredMixin, SortableListView):

    query_name = forms.CharField(max_length=25)
    query_source = forms.CharField(max_length=25)
    query_roi = forms.IntegerField()
    query_comment = forms.CharField(max_length=25)
    query_hidden = forms.BooleanField()
    query_owner = forms.CharField(max_length=25)
    query_collection_ids = forms.CharField(max_length=25)
    query_matrix_id = forms.CharField(max_length=25)
    query_tag_id = forms.CharField(max_length=25)

    query_search = forms.CharField(max_length=25)

    query_paginate_by = forms.CharField(max_length=12)

    allowed_sort_fields = {'image_name': {'default_direction': '', 'verbose_name': 'Name'},
                           'image_ordering': {'default_direction': '', 'verbose_name': 'Ordering'},
                           'image_comment': {'default_direction': '', 'verbose_name': 'Comment'},
                           'image_roi': {'default_direction': '', 'verbose_name': 'ROI'},
                           'image_hidden': {'default_direction': '', 'verbose_name': 'Hidden?'},
                           'image_owner': {'default_direction': '', 'verbose_name': 'Owner'},
                           'image_tag_ids': {'default_direction': '', 'verbose_name': 'Tag'},
                           'image_source': {'default_direction': '', 'verbose_name': 'Source'},
                           'image_collection_ids': {'default_direction': '', 'verbose_name': 'Collection'},
                           'image_matrix_ids': {'default_direction': '', 'verbose_name': 'Bench'}
                           }

    default_sort_field = 'image_name'

    paginate_by = 10

    template_name = 'host/list_images.html'

    model = ImageSummary

    context_object_name = 'image_summary_list'

    def get_queryset(self):

        sort_parameter = ''

        # URL Parameters
        kwargs_collection_id = ''
        kwargs_tag_id = ''

        # Search Parameters
        search_collection_id = ''
        search_tag_id = ''

        # image_list_by_user_and_direction Parameters
        out_collection_id = ''
        out_tag_id = ''

        # Does the URL contain a Collection Id and a Tag Id
        if self.kwargs is not None and self.kwargs != {}:

            for key in self.kwargs:

                if key == 'collection_id':

                    kwargs_collection_id = self.kwargs['collection_id']

                if key == 'tag_id':

                    kwargs_tag_id = self.kwargs['tag_id']

        # Get the URL GET Parameters
        self.query_name = self.request.GET.get('name', '')
        self.query_source = self.request.GET.get('source', '')
        self.query_roi = self.request.GET.get('roi', '')
        self.query_comment = self.request.GET.get('comment', '')
        self.query_hidden = self.request.GET.get('hidden', '')
        self.query_owner = self.request.GET.get('owner', '')
        self.query_collection_ids = self.request.GET.get('collection', '')
        self.query_tag_id = self.request.GET.get('tag', '')
        self.query_bench_id = self.request.GET.get('bench', '')

        # Set the Sort Parameter
        if self.request.GET.get('sort', None) is None:

            sort_parameter = 'image_ordering'

        else:

            sort_parameter = self.request.GET.get('sort', None)

            if sort_parameter == "image_source":

                sort_parameter = "image_server_id"

            if sort_parameter == "-image_source":

                sort_parameter = "-image_server_id"

            if sort_parameter == "image_tag_id":

                sort_parameter = "image_tag_ids"

            if sort_parameter == "-image_tag_id":

                sort_parameter = "-image_tag_ids"

            if sort_parameter == "image_collection_id":

                sort_parameter = "image_collection_ids"

            if sort_parameter == "-image_collection_id":

                sort_parameter = "-image_collection_ids"

            if sort_parameter == "image_bench_id":

                sort_parameter = "image_bench_ids"

            if sort_parameter == "-image_bench_id":

                sort_parameter = "-image_bench_ids"

        # Set the Pagination Parameter
        self.query_paginate_by = self.request.GET.get('paginate_by', '')

        if self.query_paginate_by == '':

            self.query_paginate_by = self.paginate_by

        # Set the Hidden Parameter
        if self.request.GET.get('hidden', None) == 'on':

            self.query_hidden = True

        else:

            self.query_hidden = False

        # If there isn't a URL Collection Id, use the GET Collection Id
        if kwargs_collection_id == '':

            search_collection_id = self.query_collection_ids

        else:

            search_collection_id = kwargs_collection_id

        # If there isn't a URL Tag Id, use the GET Tag Id
        if kwargs_tag_id == '':

            search_tag_id = self.query_tag_id

        else:

            search_tag_id = kwargs_tag_id

        # Check for Zero Collection id
        if search_collection_id == '0':

            out_collection_id = ''

        else:

            out_collection_id = search_collection_id

        # Check for Zero Tag Id
        if search_tag_id == '0':

            out_tag_id = ''

        else:

            out_tag_id = search_tag_id

        return image_list_by_user_and_direction(self.request.user,
                                                sort_parameter,
                                                self.query_name,
                                                self.query_source,
                                                self.query_roi,
                                                self.query_comment,
                                                self.query_hidden,
                                                self.query_owner,
                                                out_collection_id,
                                                self.query_bench_id,
                                                out_tag_id)

    def get_context_data(self, **kwargs):

        # URL Parameters
        kwargs_collection_id = ''
        kwargs_tag_id = ''

        # Search Parameters
        search_collection_id = ''
        search_tag_id = ''

        context = super().get_context_data(**kwargs)

        # Does the URL contain a Collection Id and a Tag Id
        if self.kwargs is not None and self.kwargs != {}:

            for key in self.kwargs:

                if key == 'collection_id':

                    kwargs_collection_id = self.kwargs['collection_id']

                if key == 'tag_id':

                    kwargs_tag_id = self.kwargs['tag_id']            

        # If there isn't a URL Collection Id, use the GET Collection Id
        if kwargs_collection_id == '':

            search_collection_id = self.query_collection_ids

        else:

            search_collection_id = kwargs_collection_id

        # If there isn't a URL Tag Id, use the GET Tag Id
        if kwargs_tag_id == '':

            search_tag_id = self.query_tag_id

        else:

            search_tag_id = kwargs_tag_id

        collection = None
        tag = None

        collection_image_list = []
        collection_hidden_image_list = []

        int_collection_id = 0
        int_tag_id = 0

        collection_id_formatted = ''

        if search_collection_id != '':

            allBoolean = False

            int_collection_id = int(search_collection_id)

            if int_collection_id != 0:

                collection = Collection.objects.get_or_none(id=int_collection_id)
                collection_image_list = collection.get_images()
                collection_hidden_image_list = collection.get_hidden_images()
                collection_id_formatted = collection.get_formatted_id()

        if search_tag_id != '':

            tagBoolean = True

            int_tag_id = int(search_tag_id)

            if int_tag_id != 0:

                tag = get_or_none_tag(int_tag_id)

        allBoolean = True
        tagBoolean = True

        if tag is None:

            if collection is None:

                allBoolean = True
                tagBoolean = False

            else:

                allBoolean = False
                tagBoolean = False

        else:

            if collection is None:

                allBoolean = True
                tagBoolean = True

            else:

                allBoolean = False
                tagBoolean = True

        data = get_header_data(self.request.user)

        readBoolean = False

        credential = Credential.objects.get_or_none(username=self.request.user.username)

        if credential:

            readBoolean = True

        data_dict = {'name': self.query_name,
                     'source': self.query_source,
                     'roi': self.query_roi,
                     'comment': self.query_comment,
                     'hidden': self.query_hidden,
                     'owner': self.query_owner,
                     'collection': self.query_collection_ids,
                     'bench': self.query_bench_id,
                     'tag': self.query_tag_id,
                     'paginate_by': self.query_paginate_by}

        form = ImageSummarySearchForm(data_dict, request=self.request)

        data.update({'form': form,
                     'tagBoolean': tagBoolean,
                     'allBoolean': allBoolean,
                     'readBoolean': readBoolean,
                     'collection_id': int_collection_id,
                     'collection_id_formatted': collection_id_formatted,
                     'tag': tag,
                     'collection': collection,
                     'tag_id': int_tag_id,
                     'collection_image_list': collection_image_list,
                     'collection_hidden_image_list': collection_hidden_image_list})

        context.update(data)

        return context

    def get_paginate_by(self, queryset):

        return self.request.GET.get("paginate_by", self.paginate_by)
