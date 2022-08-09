#!/usr/bin/python3
###!
# \file         delete_image.py
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
# This file contains the delete_image view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Collection
from matrices.models import Image

from matrices.routines import credential_exists
from matrices.routines import exists_image_in_cells
from matrices.routines import get_header_data


#
# DELETE AN IMAGE FROM THE ACTIVE COLLECTION
#
@login_required
def delete_image(request, image_id):

    data = get_header_data(request.user)

    if credential_exists(request.user):

        image = get_object_or_404(Image, pk=image_id)

        if exists_image_in_cells(image):

            messages.error(request, 'CPW_WEB:0790 Image ' + str(image.id) + ' NOT deleted - Still referenced in Benches!')

        else:

            list_collections = image.collections.all()

            for collection in list_collections:

                Collection.unassign_image(image, collection)

            messages.success(request, 'Image ' + str(image.id) + ' DELETED from the Workbench!')

            image.delete()

        return HttpResponseRedirect(reverse('view_all_collections', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
