#!/usr/bin/python3
###!
# \file         new_blog_credential.py
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
# This file contains the new_blog_credential view routine
#
###
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Credential

from matrices.forms import CredentialForm

from matrices.routines import get_header_data

HTTP_POST = 'POST'

#
# ADD A NEW USER BLOG CREDENTIAL
#
@login_required
def new_blog_credential(request):

    if request.user.is_superuser:

        data = get_header_data(request.user)

        if request.method == HTTP_POST:

            form = CredentialForm(request.POST)

            if form.is_valid:

                credential = form.save(commit=False)

                credential.set_owner(request.user)

                credential.save()

                messages.success(request, 'NEW Credential ' + str(credential.id) + ' Created!')

                return HttpResponseRedirect(reverse('authorisation', args=()))

            else:

                messages.error(request, "CPW_WEB:0030 New Credential - Form is Invalid!")
                form.add_error(None, "CPW_WEB:0030 New Credential - Form is Invalid!")

                data.update({ 'form': form })

        else:

            form = CredentialForm()

            data.update({ 'form': form })

        return render(request, 'authorisation/new_blog_credential.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
