#!/usr/bin/python3
###!
# \file         edit_environment.py
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
# This file contains the edit_environment view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import EnvironmentForm

from matrices.models import Environment

from matrices.routines import get_header_data
from matrices.routines import exists_primary_environment


ENVIRONMENT_NAME_CPW = 'CPW'

HTTP_POST = 'POST'


#
# EDIT AN ENVIRONMENT
#
@login_required
def edit_environment(request, environment_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        environment = get_object_or_404(Environment, pk=environment_id)

        environment_old_name = environment.name

        if request.method == HTTP_POST:

            form = EnvironmentForm(request.POST, instance=environment)

            if form.is_valid():

                if environment_old_name == ENVIRONMENT_NAME_CPW:

                    if environment.is_cpw():

                        environment = form.save(commit=False)

                        environment.set_owner(request.user)

                        environment.save()

                        messages.success(request, 'Environment ' + environment.name + ' Updated!')

                    else:

                        messages.error(request, 'CPW_WEB:0140 Edit Environment - CANNOT Change the name of the '
                                       'Primary Environment!')
                        form.add_error(None, 'CPW_WEB:0140 Edit Environment - CANNOT Change the name of the Primary '
                                       'Environment')

                else:

                    if exists_primary_environment():

                        if environment.name == ENVIRONMENT_NAME_CPW:

                            messages.error(request, 'CPW_WEB:0140 Edit Environment - CANNOT Change to the name of '
                                           'the Primary Environment!')
                            form.add_error(None, 'CPW_WEB:0140 Edit Environment - CANNOT Change to the name of the '
                                           'Primary Environment')

                        else:

                            environment = form.save(commit=False)

                            environment.set_owner(request.user)

                            environment.save()

                            messages.success(request, 'Environment ' + environment.name + ' Updated!')

                    else:

                        environment = form.save(commit=False)

                        environment.set_owner(request.user)

                        environment.save()

                        messages.success(request, 'Environment ' + environment.name + ' Updated!')

                return HttpResponseRedirect(reverse('maintenance', args=()))

            else:

                messages.error(request, 'CPW_WEB:0140 Edit Environment - Form is Invalid!')
                form.add_error(None, 'CPW_WEB:0140 Edit Environment - Form is Invalid!')

                data.update({'form': form, 'environment': environment})

        else:

            form = EnvironmentForm(instance=environment)

            data.update({'form': form, 'environment': environment})

        return render(request, 'maintenance/edit_environment.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
