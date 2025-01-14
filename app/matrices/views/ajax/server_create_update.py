#!/usr/bin/python3
#
# ##
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
# This file contains the AJAX server_create_update view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from decouple import config

from matrices.models import Credential
from matrices.models import Server

from matrices.forms import ServerForm

from matrices.routines import AESCipher
from matrices.routines import exists_server_for_uid_url
from matrices.routines import is_request_ajax


#
#   ADD or EDIT AN IMAGE SERVER
#
@login_required()
def server_create_update(request, server_id=None):

    if request.user.username == 'guest':

        raise PermissionDenied

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    object = None

    if server_id is None:
        # "Add" mode

        object = None

    else:
        # "Change" mode

        object = Server.objects.get_or_none(id=server_id)

        if object:

            if not request.user.is_superuser:

                if object.owner != request.user:

                    raise PermissionDenied

        else:

            raise PermissionDenied

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        form = ServerForm(instance=object, data=request.POST)

        if form.is_valid():

            object = form.save(commit=False)

            cipher = AESCipher(config('CPW_CIPHER_STRING'))

            encryptedPwd = cipher.encrypt(object.pwd).decode()

            object.set_pwd(encryptedPwd)
            object.set_owner(request.user)

            if server_id is None:

                # "Add" mode

                if exists_server_for_uid_url(object.uid, object.url_server):

                    messages.error(request, "CPW_WEB:0610 NEW Server - A Server already Exist for that User Id and URL!")
                    form.add_error(None, "CPW_WEB:0610 NEW Server - A Server already Exist for that User Id and URL!")

                else:

                    object.save()

                    messages.success(request, 'Server ' + str(object.id) + ' Added!')

            else:

                # "Change" mode

                object.save()

                messages.success(request, 'Server ' + str(object.id) + ' Updated!')

    else:

        form = ServerForm(instance=object)

    return render(request, template_name, {'form': form,
                                           'object': object})
