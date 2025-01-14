#!/usr/bin/python3
#
# ##
# \file         blogform.py
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
# Form for adding/editing WORDPRESS API Commands.
# ##
#
from __future__ import unicode_literals

from django import forms

from matrices.models import Protocol
from matrices.models import Blog


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ('name', 'protocol', 'application', 'preamble', 'postamble', )
        protocol = forms.ModelChoiceField(queryset=Protocol.objects.all())

    def __init__(self, *args, **kwargs):

        super(BlogForm, self).__init__(*args, **kwargs)

        self.fields['protocol'].label_from_instance = lambda obj: "{0}".format(obj.name)
