#!/usr/bin/python3
###!
# \file         delete_image_link.py
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
# This file contains the delete_image_link view routine
#
###
from __future__ import unicode_literals

import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Artefact
from matrices.models import ImageLink

from matrices.routines import credential_exists
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_header_data


#
# DELETE AN IMAGE LINK
#
@login_required
def delete_image_link(request, image_link_id):

    data = get_header_data(request.user)

    if credential_exists(request.user):

        collection_list = get_active_collection_for_user(request.user)

        collection = collection_list[0]

        image_link = get_object_or_404(ImageLink, pk=image_link_id)

        if image_link.is_owned_by(request.user) or request.user.is_superuser:

            artefact = get_object_or_404(Artefact, pk=image_link.artefact.id)

            if artefact.has_location():

                rm_command = 'rm ' + str(artefact.location)

                process = subprocess.Popen(rm_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

            messages.success(request, 'Image Link ' + str(image_link.id) + ' DELETED from the Workbench!')

            image_link.delete()

            artefact.delete()

        else:

            messages.error(request, 'Image Link ' + str(image_link.id) + ' NOT DELETED from the Workbench!')

        return HttpResponseRedirect(reverse('link_images', args=(0, 0, collection.id)))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
