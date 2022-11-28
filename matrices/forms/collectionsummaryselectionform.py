#!/usr/bin/python3
###!
# \file         collectionsummaryselectionform.py
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
# Form for selecting a collection.
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from matrices.models import Collection
from matrices.models import Profile

from matrices.routines import collection_list_by_user_and_direction


class CollectionSummarySelectionForm(forms.ModelForm):

    class Meta:
        model = Profile
        last_used_collection = forms.ModelChoiceField(queryset=Collection.objects.all(), label='Last Used Collection')
        fields = ('last_used_collection', )

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request')

        super(CollectionSummarySelectionForm, self).__init__(*args, **kwargs)

        collection_summary_queryset = collection_list_by_user_and_direction(self.request.user, 'collection_id', '', '', '', '')

        collection_queryset = Collection.objects.none()

        list_of_collection_ids = []

        for collection_summary in collection_summary_queryset:

            list_of_collection_ids.append(collection_summary.collection_id)

        collection_queryset = Collection.objects.filter(id__in=list_of_collection_ids)

        self.fields['last_used_collection'].queryset = collection_queryset
