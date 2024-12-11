#!/usr/bin/python3
#
# ##
# \file         add_ebi_sca_image.py
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
# This file contains the add_image view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse

from matrices.models import Server
from matrices.models import Credential

from matrices.routines import add_image_to_collection


#
#   ADD A NEW IMAGE FROM AN EBI SCA SERVER TO THE ACTIVE COLLECTION
#
@login_required
def add_ebi_sca_image(request, server_id, image_id, path_from):

    if request.user.username == 'guest':

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        server = Server.objects.get_or_none(id=server_id)

        if server:

            if request.user.profile.has_active_collection():

                collection = request.user.profile.active_collection

                image = add_image_to_collection(request.user, server, image_id, 0, collection.id)

                messages.success(request, 'Image ' + str(image.id) + ' ADDED to Active Collection!')

            else:

                messages.error(request, "CPW_WEB:0440 Add EBI SCA - You have no Active Image Collection; Please create a Collection!")

                return HttpResponseRedirect(reverse('home', args=()))

            if server.is_ebi_sca():

                if path_from == "show_ebi_sca_image":

                    return HttpResponseRedirect(reverse('webgallery_show_ebi_sca_image', args=(server_id, image_id)))

                if path_from == "show_ebi_sca_upload_image":

                    return HttpResponseRedirect(reverse('webgallery_show_ebi_sca_upload_image', args=(server_id, image_id)))

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
