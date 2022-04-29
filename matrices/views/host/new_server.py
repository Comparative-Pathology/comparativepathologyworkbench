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
# This file contains the new_server view routine
#
###
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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
# ADD A NEW IMAGE SERVER
#
@login_required
def new_server(request):

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        if request.user.is_superuser:

            if request.method == HTTP_POST:

                form = ServerForm(request.POST)

                if form.is_valid():

                    server = form.save(commit=False)

                    server.set_owner(request.user)

                    cipher = AESCipher(config('NOT_EMAIL_HOST_PASSWORD'))

                    encryptedPwd = cipher.encrypt(server.pwd).decode()

                    server.set_pwd(encryptedPwd)

                    server.save()

                    messages.success(request, 'NEW Server ' + str(server.id) + ' Created!')

                    return HttpResponseRedirect(reverse('list_imaging_hosts', args=()))

                else:

                    messages.error(request, "CPW_WEB:0080 New Server - Form is Invalid!")
                    form.add_error(None, "CPW_WEB:0080 New Server - Form is Invalid!")

                    data.update({ 'form': form,  })

            else:

                form = ServerForm()

                data.update({ 'form': form,  })

            return render(request, 'host/new_server.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))
