#!/usr/bin/python3
###!
# \file         views_authorisation.py
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
# This file contains the edit_user view routine
#
###
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from matrices.forms import EditUserForm

from matrices.routines import get_header_data

HTTP_POST = 'POST'

#
# EDIT A USER
#
@login_required
def edit_user(request, user_id):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        subject = get_object_or_404(User, pk=user_id)

        data.update({ 'subject': subject })

        user = get_object_or_404(User, pk=request.user.id)

        if request.method == HTTP_POST:

            form = EditUserForm(request.POST, instance=subject)

            if form.is_valid():

                user = form.save(commit=False)

                user.save()

                return HttpResponseRedirect(reverse('authorisation', args=()))

            else:

                messages.error(request, "Edit User Form is Invalid!")
                form.add_error(None, "Edit User Form is Invalid!")

                data.update({ 'form': form })

        else:

            form = EditUserForm(instance=subject)

            data.update({ 'form': form })

        return render(request, 'authorisation/edit_user.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
