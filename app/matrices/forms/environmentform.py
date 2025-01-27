#!/usr/bin/python3
# 
# ##
# \file         environmentform.py
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
# Form for adding/editing Environments.
# ##
#
from __future__ import unicode_literals

from django import forms

from matrices.models import Environment
from matrices.models import Protocol
from matrices.models import Location
from matrices.models import Gateway


class EnvironmentForm(forms.ModelForm):

    class Meta:
        model = Environment
        fields = ('name', 'location', 'protocol', 'web_root', 'document_root', 'nginx_private_location',
                  'wordpress_web_root', 'wordpress_active', 'from_email', 'date_format', 'minimum_cell_height',
                  'maximum_cell_height', 'minimum_cell_width', 'maximum_cell_width', 'maximum_initial_columns',
                  'minimum_initial_columns', 'maximum_initial_rows', 'minimum_initial_rows', 'maximum_rest_columns',
                  'minimum_rest_columns', 'maximum_rest_rows', 'minimum_rest_rows', 'maximum_bench_count',
                  'maximum_collection_count', 'gateway', 'gateway_port', 'gateway_pagination', 'background_processing',
                  'window_refresh_time', 'task_pause_time')
        location = forms.ModelChoiceField(queryset=Location.objects.all())
        protocol = forms.ModelChoiceField(queryset=Protocol.objects.all())
        gateway = forms.ModelChoiceField(queryset=Gateway.objects.all())

    def __init__(self, *args, **kwargs):

        super(EnvironmentForm, self).__init__(*args, **kwargs)

        self.fields['location'].label_from_instance = lambda obj: "{0}".format(obj.name)
        self.fields['protocol'].label_from_instance = lambda obj: "{0}".format(obj.name)
        self.fields['gateway'].label_from_instance = lambda obj: "{0}".format(obj.name)
