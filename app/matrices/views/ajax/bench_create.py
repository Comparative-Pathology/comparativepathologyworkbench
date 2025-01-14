#!/usr/bin/python3
#
# ##
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
# This file contains the AJAX bench_create view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from matrices.forms import NewMatrixForm

from matrices.models import Credential

from matrices.routines import bench_creation_consequences
from matrices.routines import get_bench_count_for_user
from matrices.routines import get_primary_cpw_environment
from matrices.routines import is_request_ajax

WORDPRESS_SUCCESS = 'Success!'


#
#   Add a New Bench
#
@login_required()
def bench_create(request):

    if not is_request_ajax(request):

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    environment = get_primary_cpw_environment()

    object = None

    template_name = 'frontend_forms/generic_form_inner.html'

    if request.method == 'POST':

        form = NewMatrixForm(instance=object, data=request.POST)

        if get_bench_count_for_user(request.user) >= environment.maximum_bench_count and \
           request.user.username == 'guest':

            messages.error(request, "CPW_WEB:0600 New Bench  - Too Many Benches for Guest User!")
            form.add_error(None, "CPW_WEB:0600 New Bench  - Too Many Benches for Guest User!")

        else:

            if form.is_valid():

                object = form.save(commit=False)

                rows = form.cleaned_data['rows']
                columns = form.cleaned_data['columns']

                number_headers = form.cleaned_data['number_headers']

                rows = rows + 1
                columns = columns + 1

                object.set_owner(request.user)

                post_id = ''

                if environment.is_wordpress_active():

                    if credential.has_apppwd():

                        returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                                 object.title,
                                                                                 object.description)

                        if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                            post_id = returned_blogpost['id']

                            object.set_blogpost(post_id)

                            object.save()

                            bench_creation_consequences(object, columns, rows, number_headers)

                            messages.success(request, 'NEW Bench ' + object.get_formatted_id() + ' Created!')

                        else:

                            messages.error(request, "CPW_WEB:0320 New Bench  - WordPress Error, "
                                           "Contact System Administrator!")
                            form.add_error(None, "CPW_WEB:0320 New Bench  - WordPress Error, "
                                           "Contact System Administrator!")

                    else:

                        messages.error(request, "CPW_WEB:0300 New Bench  - No WordPress Credentials, "
                                       "Contact System Administrator!")
                        form.add_error(None, "CPW_WEB:0300 New Bench  - No WordPress Credentials, "
                                       "Contact System Administrator!")

                else:

                    object.set_blogpost(post_id)

                    object.save()

                    bench_creation_consequences(object, columns, rows, number_headers)

                    messages.success(request, 'NEW Bench ' + object.get_formatted_id() + ' Created!')

    else:

        form = NewMatrixForm()

    return render(request, template_name, {'form': form,
                                           'object': object})
