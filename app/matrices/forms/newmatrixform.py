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
from django.core.exceptions import ValidationError

from matrices.models import Matrix

from matrices.routines import get_primary_cpw_environment


#
#   New Bench Form
#
class NewMatrixForm(forms.ModelForm):
    columns = forms.IntegerField(initial=1)
    rows = forms.IntegerField(initial=1)
    number_headers = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = Matrix
        fields = ('title', 'description', 'height', 'width')

    def clean(self):

        cleaned_data = super().clean()

        environment = get_primary_cpw_environment()

        title = cleaned_data.get("title")
        description = cleaned_data.get("description")
        height = cleaned_data.get("height")
        width = cleaned_data.get("width")
        columns = cleaned_data.get("columns")
        rows = cleaned_data.get("rows")
        number_headers = cleaned_data.get("number_headers")

        if not title:
            msg = "Please Supply a Title!"
            raise ValidationError(msg)

        if not description:
            msg = "Please Supply a Description!"
            raise ValidationError(msg)

        if height < environment.minimum_cell_height:
            msg = "Bench Cell Height is TOO small! Enter a value GREATER than "
            + str(environment.minimum_cell_height) + " Pixels"
            raise ValidationError(msg)

        if height > environment.maximum_cell_height:
            msg = "Bench Cell Height is TOO great! Enter a value LESS than "
            + str(environment.maximum_cell_height) + " Pixels"
            raise ValidationError(msg)

        if width < environment.minimum_cell_width:
            msg = "Bench Cell Width is TOO small! Enter a value GREATER than "
            + str(environment.minimum_cell_width) + " Pixels"
            raise ValidationError(msg)

        if width > environment.maximum_cell_width:
            msg = "Bench Cell Width is TOO great! Enter a value LESS than "
            + str(environment.maximum_cell_width) + " Pixels"
            raise ValidationError(msg)

        if rows > environment.maximum_initial_rows:
            msg = "TOO many Rows! Enter a value LESS than "
            + str(environment.maximum_initial_rows)
            raise ValidationError(msg)

        if columns > environment.maximum_initial_columns:
            msg = "TOO many Columns! Enter a value LESS than "
            + str(environment.maximum_initial_columns)
            raise ValidationError(msg)

        if rows < environment.minimum_initial_rows:
            msg = "TOO few Rows! Enter a value GREATER than "
            + str(environment.minimum_initial_rows)
            raise ValidationError(msg)

        if columns < environment.minimum_initial_columns:
            msg = "TOO few Columns! Enter a value GREATER than "
            + str(environment.minimum_initial_columns)
            raise ValidationError(msg)
