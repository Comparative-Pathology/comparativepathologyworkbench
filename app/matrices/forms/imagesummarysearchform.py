#!/usr/bin/python3
###!
# \file         imagesummarysearchform.py
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
# Form for searching Images.
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from matrices.models import Image
from matrices.models import Server
from matrices.models import Collection
from matrices.models import Matrix

from taggit.models import Tag

from matrices.routines import collection_list_by_user_and_direction
from matrices.routines import bench_list_by_user_and_direction

CHOICES = (('10', '10'), ('1', '1'), ('5', '5'), ('25', '25'), ('50', '50'), ('100', '100'))


class ImageSummarySearchForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=False)
    roi = forms.IntegerField(required=False)
    comment = forms.CharField(max_length=50, required=False)
    hidden = forms.BooleanField(initial=False, required=False)
    owner = forms.ModelChoiceField(queryset=User.objects.all().order_by('id'), required=False, empty_label="(All Owners)")
    source = forms.ModelChoiceField(queryset=Server.objects.all().order_by('id'), required=False, empty_label="(All Sources)")
    collection = forms.ModelChoiceField(queryset=Collection.objects.all().order_by('id'), required=False, empty_label="(All Collections)")
    bench = forms.ModelChoiceField(queryset=Matrix.objects.all().order_by('id'), required=False, empty_label="(All Benches)", )
    tag = forms.ModelChoiceField(queryset=None, required=False, empty_label="(All Tags)", to_field_name="id")
    paginate_by = forms.ChoiceField(widget=forms.Select, choices=CHOICES, required=False)

    class Meta:
        model = Image
        fields = ('name',
                'comment',
                'roi',
                'hidden',
                'source',
                'collection',
                'bench',
                'paginate_by',
                'owner',
                'tag',
                )

    def __init__(self, *args, **kwargs):

        request = kwargs.pop('request')

        query_tag_id = request.GET.get('tag', '')

        full_path = request.get_full_path()[1:-1]

        param_collection_id = '0'
        param_tag_id = '0'

        # Extract the Parameters from the URL
        if "/" in full_path:

            full_path_array = full_path.split("/", 3)

            if len(full_path_array) == 2:

                parameter_1 = full_path_array[1]

                if parameter_1[0] != '?':
                        
                    param_collection_id = full_path_array[1]

            if len(full_path_array) >= 3:

                param_collection_id = full_path_array[1]

                parameter_2 = full_path_array[2]

                if parameter_2[0] != '?':
                        
                    param_tag_id = full_path_array[2]

        dict_args = args[0]

        super(ImageSummarySearchForm, self).__init__(*args, **kwargs)

        self.fields['source'].label_from_instance = lambda obj: "{0}".format(obj.name)
        self.fields['collection'].label_from_instance = lambda obj: "{0:06d}, {1}, {2}".format(obj.id, obj.owner.username, obj.title)
        self.fields['bench'].label_from_instance = lambda obj: "CPW:{0:06d}, {1}".format(obj.id, obj.title)


        # Update the Collection Selection Box to Only show Collections that the user has access to
        collection_summary_queryset = collection_list_by_user_and_direction(request.user, 'collection_id', '', '', '', '', '')


        collection_queryset = Collection.objects.none()

        list_of_collection_ids = []

        if param_collection_id == '0':

            for collection_summary in collection_summary_queryset:

                list_of_collection_ids.append(collection_summary.collection_id)

        else:

            list_of_collection_ids.insert(0, param_collection_id)
            self.fields['collection'].empty_label = None

        collection_queryset = Collection.objects.filter(id__in=list_of_collection_ids).order_by('id')

        self.fields['collection'].queryset = collection_queryset


        # Update the Bench Selection Box to Only show Benches that the user has access to
        bench_summary_queryset = bench_list_by_user_and_direction(request.user, '', '', '', '', '', '', '', '', '', '')

        bench_queryset = Matrix.objects.none()

        list_of_bench_ids = []

        for bench_summary in bench_summary_queryset:

            list_of_bench_ids.append(bench_summary.matrix_id)

        bench_queryset = Matrix.objects.filter(id__in=list_of_bench_ids).order_by('id')

        self.fields['bench'].queryset = bench_queryset

        # Update the Tag Selection Box to show all available Tags
        tag_queryset = Tag.objects.all()
        self.fields['tag'].queryset = tag_queryset


        if not request.user.is_superuser:

            # Hide the Owner Search Selection box for ordinary users
            self.fields['owner'].widget = forms.HiddenInput()
