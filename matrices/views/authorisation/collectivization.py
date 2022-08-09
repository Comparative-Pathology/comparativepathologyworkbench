#!/usr/bin/python3
###!
# \file         collectivization.py
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
# This file contains the collectivization view routine
#
###
from __future__ import unicode_literals

from django.http import HttpResponseRedirect

from django.shortcuts import render

from django.contrib.auth.models import User

from matrices.models import Collection

from matrices.routines import exists_active_collection_for_user
from matrices.routines import exists_image_for_user
from matrices.routines import get_header_data
from matrices.routines import get_images_for_user

#
# SETUP DEFAULT COLLECTIONS VIEW
#
def collectivization(request):

    data = get_header_data(request.user)

    if request.user.is_superuser:

        user_list = User.objects.all()

        out_message_list = list()

        for user in user_list:

            imageCount = 0

            out_message = ""

            if exists_image_for_user(user):

                image_list = get_images_for_user(user)

                if exists_active_collection_for_user(user):

                    out_message = "Default Collection ALREADY exists for User {}".format( user.username )

                else:

                    collection = Collection.create("Default Collection", "Default Collection", True, user)

                    collection.save()

                    for image in image_list:

                        imageCount = imageCount + 1

                        Collection.assign_image(image, collection)

                    out_message = "Default Collection created for {} Images for User {}".format( imageCount, user.username )

            else:

                out_message = "NO Default Collection created for User {}".format( user.username )

            out_message_list.append(out_message)

        data.update({ 'out_message_list': out_message_list })

        return render(request, 'authorisation/collectivization.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
