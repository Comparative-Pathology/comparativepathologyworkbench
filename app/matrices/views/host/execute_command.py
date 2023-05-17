#!/usr/bin/python3
###!
# \file         execute_command.py
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
#
# This file contains the execute command view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Credential

from matrices.routines import get_header_data

#
# SHOW THE AUTHORISATION PAGE
#
@login_required
def execute_command(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        user_list = User.objects.all()
        credential_list = Credential.objects.all()

        data.update({ 'user_list': user_list })
        data.update({ 'credential_list': credential_list })

        return render(request, 'host/execute_command.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
