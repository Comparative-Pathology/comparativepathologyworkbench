#!/usr/bin/python3
###!
# \file         serverform.py
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
# Form for adding/editing Servers.
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.html import conditional_escape
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from matrices.models import Type
from matrices.models import Server

from matrices.routines import exists_server_for_uid_url


#
# SERVER FORM
#
class ServerForm(forms.ModelForm):

    class Meta:
        model = Server
        fields = ('name', 'url_server', 'uid', 'pwd', 'type', 'accessible')
        widgets = {
            'pwd': forms.PasswordInput(),
        }
        type = forms.ModelChoiceField(queryset=Type.objects.all())


    def clean(self):

        cleaned_data = super().clean()

        name = cleaned_data.get("name")
        url_server = cleaned_data.get("url_server")
        uid = cleaned_data.get("uid")

        if not name:
            msg = "Please Supply a Name!"
            raise ValidationError(msg)

        if not url_server:
            msg = "Please Supply a URL!"
            raise ValidationError(msg)

        if exists_server_for_uid_url(uid, url_server):
            msg = "Server already exist for supplied Uid \"" + str(uid) + "\" and URL \"" + str(url_server) + "\""
            raise ValidationError(msg)
