#!/usr/bin/python3
###!
# \file         server_create_update.py
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
# This file contains the AJAX server_create_update view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from frontend_forms.utils import get_object_by_uuid_or_404

from decouple import config

from matrices.models import Server

from matrices.forms import ServerForm

from matrices.routines import AESCipher
from matrices.routines import credential_exists
from matrices.routines import simulate_network_latency


#
# ADD or EDIT AN IMAGE SERVER
#
@login_required()
def server_create_update(request, server_id=None):

    if request.user.username == 'guest':

        raise PermissionDenied

    if not request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


    object = None

    if server_id is None:
        # "Add" mode
        object = None

    else:
        # "Change" mode
        object = get_object_by_uuid_or_404(Server, server_id)

        if not request.user.is_superuser:

            if object.owner != request.user:

                raise PermissionDenied


    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        simulate_network_latency()

        #form = ServerForm(data=request.POST)
        form = ServerForm(instance=object, data=request.POST)

        if form.is_valid():

            object = form.save(commit=False)

            cipher = AESCipher(config('NOT_EMAIL_HOST_PASSWORD'))

            encryptedPwd = cipher.encrypt(object.pwd).decode()

            object.set_pwd(encryptedPwd)

            object.set_owner(request.user)

            object.save()

            if server_id is None:
                # "Add" mode
                messages.success(request, 'Server ' + str(object.id) + ' Added!')

            else:
                # "Change" mode
                messages.success(request, 'Server ' + str(object.id) + ' Updated!')

    else:

        form = ServerForm(instance=object)

    return render(request, template_name, {
        'form': form,
        'object': object
    })
