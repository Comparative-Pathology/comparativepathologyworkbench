#!/usr/bin/python3
###!
# \file         bench_create.py
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
# This file contains the AJAX bench_create view routine
#
###
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from frontend_forms.utils import get_object_by_uuid_or_404

from decouple import config

from matrices.forms import NewMatrixForm

from matrices.models import Matrix

from matrices.routines import credential_exists
from matrices.routines import bench_creation_consequences
from matrices.routines import get_credential_for_user
from matrices.routines import get_primary_wordpress_server
from matrices.routines import simulate_network_latency

WORDPRESS_SUCCESS = 'Success!'


#
# ADD A BENCH
#
@login_required()
def bench_create(request):

    if not request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    if not credential_exists(request.user):

        raise PermissionDenied


    serverWordpress = get_primary_wordpress_server()
    credential = get_credential_for_user(request.user)

    object = None

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        simulate_network_latency()

        form = NewMatrixForm(instance=object, data=request.POST)

        if form.is_valid():

            if credential.has_apppwd():

                object = form.save(commit=False)

                rows = form.cleaned_data['rows']
                columns = form.cleaned_data['columns']

                rows = rows + 1
                columns = columns + 1

                object.set_owner(request.user)

                post_id = ''

                returned_blogpost = serverWordpress.post_wordpress_post(credential, object.title, object.description)

                if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                    post_id = returned_blogpost['id']

                    object.set_blogpost(post_id)

                    object.save()

                    bench_creation_consequences(object, columns, rows)

                    matrix_id_formatted = "CPW:" + "{:06d}".format(object.id)
                    messages.success(request, 'NEW Bench ' + matrix_id_formatted + ' Created!')

                else:

                    messages.error(request, "CPW_WEB:0370 New Bench  - WordPress Error, Contact System Administrator!")
                    form.add_error(None, "CPW_WEB:0370 New Bench  - WordPress Error, Contact System Administrator!")

            else:

                messages.error(request, "CPW_WEB:xxxx New Bench  - No WordPress Credentials, Contact System Administrator!")
                form.add_error(None, "CPW_WEB:xxxx New Bench  - No WordPress Credentials, Contact System Administrator!")

    else:

        form = NewMatrixForm()


    return render(request, template_name, {
        'form': form,
        'object': object
    })
