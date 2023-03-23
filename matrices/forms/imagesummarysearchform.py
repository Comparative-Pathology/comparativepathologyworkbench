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
    collection_id = forms.ModelChoiceField(queryset=Collection.objects.all().order_by('id'), required=False, empty_label="(All Collections)")
    bench_id = forms.ModelChoiceField(queryset=Matrix.objects.all().order_by('id'), required=False, empty_label="(All Benches)")
    paginate_by = forms.ChoiceField(widget=forms.Select, choices=CHOICES, required=False)

    class Meta:
        model = Image
        fields = ('name',
                'comment',
                'roi',
                'hidden',
                'source',
                'collection_id',
                'bench_id',
                'paginate_by',
                'owner',
                )

    def __init__(self, *args, **kwargs):

        request = kwargs.pop('request')

        full_path = request.get_full_path()[1:-1]

        param_collection_id = '0'

        if "/" in full_path:

            x = full_path.split("/", 2)
            y = x[1]

            if y[0] != '?':

                param_collection_id = x[1]

        dict_args = args[0]

        super(ImageSummarySearchForm, self).__init__(*args, **kwargs)

        if not request.user.is_superuser:

            # Hide the Owner Search Selection box
            self.fields['owner'].widget = forms.HiddenInput()


            # Update the Collection Selection Box to Only show Collecitons that the user has access to
            collection_summary_queryset = collection_list_by_user_and_direction(request.user, 'collection_id', '', '', '', '')

            collection_queryset = Collection.objects.none()

            list_of_collection_ids = []

            if param_collection_id == '0':

                for collection_summary in collection_summary_queryset:

                    list_of_collection_ids.append(collection_summary.collection_id)

            else:

                list_of_collection_ids.insert(0, param_collection_id)
                self.fields['collection_id'].empty_label = None

            collection_queryset = Collection.objects.filter(id__in=list_of_collection_ids).order_by('id')

            self.fields['collection_id'].queryset = collection_queryset


            # Update the Bench Selection Box to Only show Benches that the user has access to
            bench_summary_queryset = bench_list_by_user_and_direction(request.user, '', '', '', '', '', '', '', '', '', '')

            bench_queryset = Matrix.objects.none()

            list_of_bench_ids = []

            for bench_summary in bench_summary_queryset:

                list_of_bench_ids.append(bench_summary.matrix_id)

            bench_queryset = Matrix.objects.filter(id__in=list_of_bench_ids).order_by('id')

            self.fields['bench_id'].queryset = bench_queryset
