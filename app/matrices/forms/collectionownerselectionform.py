#!/usr/bin/python3
###!
# \file         collectionownerselectionform.py
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
# Form for selecting a new owner of a collection.
###
from __future__ import unicode_literals

from django import forms
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from matrices.models import Collection


class CollectionOwnerSelectionForm(forms.ModelForm):

    owner = forms.ModelChoiceField(queryset=User.objects.all(), required=True, empty_label=None)

    class Meta:
        model = Collection
        fields = ('owner', )
