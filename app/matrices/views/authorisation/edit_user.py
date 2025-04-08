#!/usr/bin/python3
#
# ##
# \file         edit_user.py
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
# This file contains the edit_user view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.forms import EditUserForm
from matrices.forms import EditConstrainedProfileForm

from matrices.models import Image

from matrices.routines import get_header_data
from matrices.routines import get_or_none_user

HTTP_POST = 'POST'


#
#   EDIT A USER
#
@login_required
def edit_user(request, user_id):

    if request.user.is_superuser:

        user = get_or_none_user(request.user.id)

        subject = get_or_none_user(user_id)

        if user and subject:

            data = get_header_data(request.user)

            data.update({'subject': subject})

            if request.method == HTTP_POST:

                user_form = EditUserForm(request.POST, instance=subject)
                profile_form = EditConstrainedProfileForm(request.POST, instance=subject.profile)

                if all((profile_form.is_valid(), user_form.is_valid())):

                    user = user_form.save()
                    profile = profile_form.save()

                    username = subject.username

                    column_map = {'pk': 'e.id'}

                    raw_image_queryset = Image.objects.raw('select e.id from matrices_collection a, auth_user b, \
                                                           matrices_collection_images c, matrices_cell d, \
                                                           matrices_image e where a.owner_id = b.id and \
                                                           b.username = %s and a.id = c.collection_id and \
                                                           c.image_id = d.image_id and c.image_id = e.id',
                                                           [username], translations=column_map)

                    list_of_image_ids = []

                    for image in raw_image_queryset:

                        list_of_image_ids.append(int(image.id))

                    image_queryset = Image.objects.filter(pk__in=list_of_image_ids).order_by('id')

                    image_queryset.update(hidden=profile.hide_collection_image)

                    user.save()
                    profile.save()

                    messages.success(request, 'User ' + user.username + ' Updated!')

                    return HttpResponseRedirect(reverse('authorisation', args=()))

                else:

                    messages.error(request, "CPW_WEB:0020 Edit User - Form is Invalid!")
                    user_form.add_error(None, "CPW_WEB:0020 Edit User - Form is Invalid!")

                    data.update({'user_form': user_form,
                                 'profile_form': profile_form})

            else:

                user_form = EditUserForm(instance=subject)
                profile_form = EditConstrainedProfileForm(instance=subject.profile)

                data.update({'user_form': user_form,
                             'profile_form': profile_form})

            return render(request, 'authorisation/edit_user.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
