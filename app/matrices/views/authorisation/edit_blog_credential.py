#!/usr/bin/python3
#
# ##
# \file         edit_blog_credential.py
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
# This file contains the edit_blog_credential view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Credential

from matrices.forms import CredentialForm

from matrices.routines import get_header_data

HTTP_POST = 'POST'


#
#   EDIT A USER BLOG CREDENTIAL
#
@login_required
def edit_blog_credential(request, credential_id):

    if request.user.is_superuser:

        credential = Credential.objects.get_or_none(id=credential_id)

        if credential:

            data = get_header_data(request.user)

            if request.method == HTTP_POST:

                form = CredentialForm(request.POST, instance=credential)

                if form.is_valid():

                    credential = form.save(commit=False)

                    credential.set_owner(request.user)

                    credential.save()

                    messages.success(request, 'Credential ' + str(credential.id) + ' Updated!')

                    return HttpResponseRedirect(reverse('authorisation', args=()))

                else:

                    messages.error(request, "CPW_WEB:0010 Edit Blog Credential - Form is Invalid!")
                    form.add_error(None, "CPW_WEB:0010 Edit Blog Credential - Form is Invalid!")

                    data.update({'form': form,
                                 'credential': credential})

            else:

                form = CredentialForm(instance=credential)

                data.update({'form': form,
                             'credential': credential})

            return render(request, 'authorisation/edit_blog_credential.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
