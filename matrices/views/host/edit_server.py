#!/usr/bin/python3
###!
# \file         views_host.py
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
# This file contains the edit_server view routine
#
###
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from decouple import config

from matrices.forms import ServerForm

from matrices.models import Server

from matrices.routines import AESCipher
from matrices.routines import get_header_data

HTTP_POST = 'POST'
NO_CREDENTIALS = ''

#
# EDIT AN IMAGE SERVER
#
@login_required
def edit_server(request, server_id):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if server.is_owned_by(request.user) or request.user.is_superuser:

            if request.method == HTTP_POST:

                form = ServerForm(request.POST, instance=server)

                if form.is_valid():

                    server = form.save(commit=False)

                    cipher = AESCipher(config('NOT_EMAIL_HOST_PASSWORD'))

                    encryptedPwd = cipher.encrypt(server.pwd).decode()

                    server.set_pwd(encryptedPwd)

                    server.set_owner(request.user)

                    server.save()

                    return HttpResponseRedirect(reverse('list_imaging_hosts', args=()))

                else:

                    messages.error(request, "Error")

                    data.update({ 'form': form, 'server': server })

            else:

                form = ServerForm(instance=server)

                data.update({ 'form': form, 'server': server })

            return render(request, 'host/edit_server.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))
