#!/usr/bin/python3
###!
# \file         collectionsummarysearchform.py
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
# Form for searching collections.
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from matrices.models import CollectionSummary
from matrices.models import CollectionAuthority


class CollectionSummarySearchForm(forms.ModelForm):
    title = forms.CharField(max_length=20, required=False)
    description = forms.CharField(max_length=20, required=False)
    owner = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    authority = forms.ModelChoiceField(queryset=CollectionAuthority.objects.all(), required=False)

    class Meta:
        model = CollectionSummary
        fields = ('title',
                'description',
                'owner',
                'authority',
                )
