#!/usr/bin/python3
###!
# \file         collectionform.py
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
# Form for adding/editing Collections.
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from matrices.models import Collection

from matrices.routines import exists_unique_title_for_collection_for_user
from matrices.routines import get_unique_title_for_collection_for_user


#
# COLLECTION FORM
#
class CollectionForm(forms.ModelForm):

    class Meta:
        model = Collection
        fields = ('title', 'description', 'active', )


    def __init__(self, *args, **kwargs):
        # important to "pop" added kwarg before call to parent's constructor
        self.request = kwargs.pop('request')

        if 'instance' in kwargs:
            if kwargs['instance'] is None:
                self.id = 0
            else:
                self.id = kwargs['instance'].id
        else:
            self.id = 0

        super(CollectionForm, self).__init__(*args, **kwargs)


    def clean(self):

        cleaned_data = super().clean()

        title = cleaned_data.get("title")
        description = cleaned_data.get("description")
        active = cleaned_data.get("active")

        if not title:
            msg = "Please Supply a Title!"
            raise ValidationError(msg)

        if not description:
            msg = "Please Supply a Description!"
            raise ValidationError(msg)

        if exists_unique_title_for_collection_for_user(self.request.user, title):

            if self.id == 0:

                msg = "Collection Title already exists for YOU! (CREATE)"
                raise ValidationError(msg)

            else:

                collection_existing = get_unique_title_for_collection_for_user(self.request.user, title)

                if self.id != collection_existing.id:

                    msg = "Collection Title Already exists for YOU! (UPDATE)"
                    raise ValidationError(msg)
