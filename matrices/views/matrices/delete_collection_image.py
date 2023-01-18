#!/usr/bin/python3
###!
# \file         delete_collection_image.py
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
# This file contains the delete_collection_image view routine
#
###
from __future__ import unicode_literals

import subprocess


from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Collection
from matrices.models import Image
from matrices.models import Artefact

from matrices.routines import credential_exists
from matrices.routines import exists_image_in_cells
from matrices.routines import get_header_data


#
# DELETE AN IMAGE FROM THE COLLECTION SUPPLIED
#
@login_required
def delete_collection_image(request, collection_id, image_id):

    data = get_header_data(request.user)

    if credential_exists(request.user):

        image = get_object_or_404(Image, pk=image_id)

        if exists_image_in_cells(image):

            messages.error(request, 'CPW_WEB:0530 Image ' + str(image.id) + ' NOT deleted - Still referenced in Benches!')

        else:

            list_collections = image.collections.all()

            boolAllowDelete = True

            if image.exists_image_links():

                if image.exists_parent_image_links():

                    image_link_list_parent = image.get_parent_image_links()

                    for image_link in image_link_list_parent:

                        if image_link.is_owned_by(request.user):

                            artefact = get_object_or_404(Artefact, pk=image_link.artefact.id)

                            if artefact.has_location():

                                rm_command = 'rm ' + str(artefact.location)
                                rm_escaped = rm_command.replace("(", "\(" ).replace(")", "\)" )

                                process = subprocess.Popen(rm_escaped, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                            image_link.delete()

                            artefact.delete()

                        else:

                            boolAllowDelete = False


                if image.exists_child_image_links():

                    image_link_list_child = image.get_child_image_links()

                    for image_link in image_link_list_child:

                        if image_link.is_owned_by(request.user):

                            artefact = get_object_or_404(Artefact, pk=image_link.artefact.id)

                            if artefact.has_location():

                                rm_command = 'rm ' + str(artefact.location)
                                rm_escaped = rm_command.replace("(", "\(" ).replace(")", "\)" )

                                process = subprocess.Popen(rm_escaped, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                            image_link.delete()

                            artefact.delete()

                        else:

                            boolAllowDelete = False

            if boolAllowDelete == True:

                for collection in list_collections:

                    Collection.unassign_image(image, collection)

                messages.success(request, 'Image ' + str(image.id) + ' DELETED from the Workbench!')

                if image.server.is_ebi_sca() or image.server.is_cpw():

                    image_path = settings.MEDIA_ROOT + '/' + image.name

                    rm_command = 'rm ' + str(image_path)
                    rm_escaped = rm_command.replace("(", "\(" ).replace(")", "\)" )

                    process = subprocess.Popen(rm_escaped, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                image.delete()

            else:

                messages.error(request, 'Image ' + str(image.id) + ' NOT DELETED from the Workbench!')


        return HttpResponseRedirect(reverse('view_collection', args=(collection_id, )))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
