#!/usr/bin/python3
###!
# \file         newmatrixform.py
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
# Form for adding new Benches.
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from matrices.models import Matrix

MAXIMUM_INITIAL_COLUMNS = 10
MAXIMUM_INITIAL_ROWS = 10
MINIMUM_INITIAL_COLUMNS = 1
MINIMUM_INITIAL_ROWS = 1

MINIMUM_HEIGHT = 75
MAXIMUM_HEIGHT = 450
MINIMUM_WIDTH = 75
MAXIMUM_WIDTH = 450


class NewMatrixForm(forms.ModelForm):
    columns = forms.IntegerField(initial=1)
    rows = forms.IntegerField(initial=1)

    class Meta:
        model = Matrix
        fields = ('title', 'description', 'height', 'width' )

    def clean(self):

        cleaned_data = super().clean()

        title = cleaned_data.get("title")
        description = cleaned_data.get("description")
        height = cleaned_data.get("height")
        width = cleaned_data.get("width")
        columns = cleaned_data.get("columns")
        rows = cleaned_data.get("rows")

        if not title:
            msg = "Please Supply a Title!"
            raise ValidationError(msg)

        if not description:
            msg = "Please Supply a Description!"
            raise ValidationError(msg)

        if height < MINIMUM_HEIGHT:
            msg = "Bench Cell Height is TOO small! Enter a value GREATER than 75 Pixels"
            raise ValidationError(msg)

        if height > MAXIMUM_HEIGHT:
            msg = "Bench Cell Height is TOO great! Enter a value LESS than 450 Pixels"
            raise ValidationError(msg)

        if width < MINIMUM_WIDTH:
            msg = "Bench Cell Width is TOO small! Enter a value GREATER than 75 Pixels"
            raise ValidationError(msg)

        if width > MAXIMUM_WIDTH:
            msg = "Bench Cell Width is TOO great! Enter a value LESS than 450 Pixels"
            raise ValidationError(msg)

        if rows > MAXIMUM_INITIAL_ROWS:
            msg = "TOO many Rows! Enter a value LESS than 10"
            raise ValidationError(msg)

        if columns > MAXIMUM_INITIAL_COLUMNS:
            msg = "TOO many Columns! Enter a value LESS than 10"
            raise ValidationError(msg)

        if rows < MINIMUM_INITIAL_ROWS:
            msg = "TOO few Rows! Enter a value GREATER than 1"
            raise ValidationError(msg)

        if columns < MINIMUM_INITIAL_COLUMNS:
            msg = "TOO few Columns! Enter a value GREATER than 1"
            raise ValidationError(msg)
