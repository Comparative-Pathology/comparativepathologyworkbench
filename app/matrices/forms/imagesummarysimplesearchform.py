#!/usr/bin/python3
# \file         imagesummarysimplesearchform.py
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


PAGE_CHOICES = (('10', 'Paginate By ...'),
                ('10', '10'),
                ('1', '1'),
                ('5', '5'),
                ('25', '25'),
                ('50', '50'),
                ('100', '100'))

SORT_CHOICES = (('', 'Sort By ...'),
                ('name', 'Name'),
                ('comment', 'Comment'),
                ('roi', 'ROI'),
                ('hidden', 'Hidden'),
                ('owner', 'Owner'),
                ('tag', 'Tag'),
                ('source', 'Source'),
                ('collection', 'Collection'),
                ('bench', 'Bench'))

DIRECTION_CHOICES = (('', 'Sort Direction ...'),
                     ('ascending', 'Ascending'),
                     ('descending', 'Descending'))


#
#   The ImageSummary Simple Search Form
#
class ImageSummarySimpleSearchForm(forms.Form):

    name = forms.CharField(max_length=50,
                           required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Image Search ...'}))

    sort_field = forms.ChoiceField(widget=forms.Select,
                                   choices=SORT_CHOICES,
                                   required=False)

    sort_direction = forms.ChoiceField(widget=forms.Select,
                                       choices=DIRECTION_CHOICES,
                                       required=False)

    owner = forms.ModelChoiceField(queryset=User.objects.all().order_by('id'),
                                   required=False,
                                   empty_label="(All Owners)")

    paginate_by = forms.ChoiceField(widget=forms.Select,
                                    choices=PAGE_CHOICES,
                                    required=False)

    class Meta:
        fields = ('name',
                  'sort_field',
                  'sort_direction',
                  'owner',
                  'paginate_by',
                  )

    def __init__(self, *args, **kwargs):

        request = kwargs.pop('request')

        super(ImageSummarySimpleSearchForm, self).__init__(*args, **kwargs)

        if not request.user.is_superuser:

            # Hide the Owner Search Selection box for ordinary users
            self.fields['owner'].widget = forms.HiddenInput()
