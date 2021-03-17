#!/usr/bin/python3
###!
# \file         collectionauthorisationform.py
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
# Form for adding/editing Collection Auhorisations.
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from matrices.models import Collection
from matrices.models import CollectionAuthority
from matrices.models import CollectionAuthorisation


class CollectionAuthorisationForm(forms.ModelForm):

    collection = forms.ModelChoiceField(queryset=Collection.objects.all())
    permitted = forms.ModelChoiceField(queryset=User.objects.all())
    collection_authority = forms.ModelChoiceField(queryset=CollectionAuthority.objects.all())

    class Meta:
        model = CollectionAuthorisation
        fields = ('collection', 'permitted', 'collection_authority', )
