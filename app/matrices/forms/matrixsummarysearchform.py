#!/usr/bin/python3
###!
# \file         matrixsummarysearchform.py
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
# Form for searching Benches.
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User

from matrices.models import MatrixSummary
from matrices.models import Authority

CHOICES = (('10', '10'),
           ('5', '5'),
           ('25', '25'),
           ('50', '50'),
           ('100', '100'))


class MatrixSummarySearchForm(forms.ModelForm):

    title = forms.CharField(max_length=20,
                            required=False)
    description = forms.CharField(max_length=20,
                                  required=False)
    created_before = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
                                         required=False)
    created_after = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
                                        required=False)
    modified_before = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
                                          required=False)
    modified_after = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'],
                                         required=False)
    owner = forms.ModelChoiceField(queryset=User.objects.all(),
                                   required=False,
                                   empty_label="(All Owners)")
    authority = forms.ModelChoiceField(queryset=Authority.objects.all(),
                                       required=False,
                                       empty_label="(All Permissions)")
    paginate_by = forms.ChoiceField(widget=forms.Select,
                                    choices=CHOICES,
                                    required=False)

    class Meta:
        model = MatrixSummary
        fields = ('title',
                  'description',
                  'owner',
                  'authority',
                  'paginate_by',
                  'created_before',
                  'created_after',
                  'modified_before',
                  'modified_after',
                  )

    def __init__(self, *args, **kwargs):

        super(MatrixSummarySearchForm, self).__init__(*args, **kwargs)

        self.fields['owner'].label_from_instance = lambda obj: "{0}".format(obj.username)
        self.fields['authority'].label_from_instance = lambda obj: "{0}".format(obj.name)
