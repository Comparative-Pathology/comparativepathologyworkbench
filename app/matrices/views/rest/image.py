#!/usr/bin/python3
#
# ##
# \file         image.py
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
# The Image View Set automatically provides `list`, `create`, `retrieve`,
# `update` and `destroy` actions.
# ##
#
from __future__ import unicode_literals

import subprocess

from rest_framework import permissions, viewsets
from rest_framework.response import Response

from matrices.models import Collection
from matrices.models import Image
from matrices.models import Artefact

from matrices.permissions import ImageIsReadOnlyOrIsAdminOrIsOwner

from matrices.serializers import ImageSerializer

from matrices.routines import exists_image_in_cells


class ImageViewSet(viewsets.ModelViewSet):
    """A ViewSet of Images

    This viewset automatically provides:
        List, Create, Retrieve, Update and Destroy actions for Images.

    Parameters:
        None

    """

    queryset = Image.objects.all()

    serializer_class = ImageSerializer

    # Check that the user is allowed permission to use the Image View Set
    permission_classes = (permissions.IsAuthenticated,
                          ImageIsReadOnlyOrIsAdminOrIsOwner)

    def partial_update(self, request, *args, **kwargs):
        """Partial Update Image.

        A Partial Update of a Image is NOT Allowed

        Parameters:

        Returns:

        Raises:

        """

        return Response(data='Image PARTIAL UPDATE Not Available')

    def list(self, request, *args, **kwargs):
        """List Images.

        Listing Images is NOT Allowed

        Parameters:

        Returns:

        Raises:

        """

        return Response(data='Image LIST Not Available')

    def destroy(self, request, *args, **kwargs):
        """Destroy Image.

        This fucntion destroys the requested Image.

        Parameters:

        Returns:

        Raises:

        """

        image = self.get_object()

        responseMsg = 'Image Deletion Response Message'

        # Check if the Image is still referenced in a Cell
        #  Yes
        if exists_image_in_cells(image):

            #  Image Deletion is NOT allowed for Images still referenced in a Bench
            responseMsg = 'Image Deletion NOT Allowed - Image still referenced in a Bench!'

        # No
        else:

            boolAllowDelete = True

            # Is the Image from a WordPress or OMERO server ... ?
            #  Yes
            if image.server.is_wordpress() or image.server.is_omero547():

                # Does the Image have any Image Links ... ?
                #  Yes
                if image.exists_image_links():

                    # Does the Image have any Parent Image Links ... ?
                    #  Yes
                    if image.exists_parent_image_links():

                        # Get all the image links that are Parents of this Image
                        image_link_list_parent = image.get_parent_image_links()

                        # Process all the image links that are Parents of this Image
                        for image_link in image_link_list_parent:

                            # Does the Requesting User own this Image Link or is the Requesting User an Admin ... ?
                            #  Yes
                            if image_link.is_owned_by(request.user) or request.user.is_superuser:

                                # Get the Artefact associated with this Image Link
                                artefact = Artefact.objects.get_or_none(id=image_link.artefact.id)

                                # Is there an Artefact ... ?
                                #  Yes
                                if artefact:

                                    # Does the Image Link have a file location
                                    if artefact.has_location():

                                        rm_command = 'rm ' + str(artefact.location)

                                        # Delete the located file for this artefact
                                        process = subprocess.Popen(rm_command,
                                                                   shell=True,
                                                                   stdout=subprocess.PIPE,
                                                                   stderr=subprocess.PIPE,
                                                                   universal_newlines=True)

                                    # Delete the Image Link
                                    image_link.delete()

                                    # Delete the Artefact
                                    artefact.delete()

                                # No
                                else:

                                    # Delete the Image Link
                                    image_link.delete()

                            # No, disallow the Image deletion
                            else:

                                boolAllowDelete = False

                    # Does the Image have any Parent Image Links ... ?
                    #  Yes
                    if image.exists_child_image_links():

                        # Get all the image links that are Children of this Image
                        image_link_list_child = image.get_child_image_links()

                        # Process all the image links that are Children of this Image
                        for image_link in image_link_list_child:

                            # Does the Requesting User own this Image Link or is the Requesting User an Admin ... ?
                            #  Yes
                            if image_link.is_owned_by(request.user) or request.user.is_superuser:

                                # Get the Artefact associated with this Image Link
                                artefact = Artefact.objects.get_or_none(id=image_link.artefact.id)

                                # Is there an Artefact ... ?
                                #  Yes
                                if artefact:

                                    # Does the Image Link have a file location
                                    if artefact.has_location():

                                        rm_command = 'rm ' + str(artefact.location)

                                        # Delete the located file for this artefact
                                        process = subprocess.Popen(rm_command,
                                                                   shell=True,
                                                                   stdout=subprocess.PIPE,
                                                                   stderr=subprocess.PIPE,
                                                                   universal_newlines=True)

                                    # Delete the Image Link
                                    image_link.delete()

                                    # Delete the Artefact
                                    artefact.delete()

                                #  No
                                else:

                                    # Delete the Image Link
                                    image_link.delete()

                            else:

                                # No, disallow the Image deletion
                                boolAllowDelete = False

                #  Can we delete this image ... ?
                #  Yes ... 
                if boolAllowDelete is True:

                    #  Get all the collections that have this Image
                    list_collections = image.collections.all()

                    #  Process all the Collections that hold this image
                    for collection in list_collections:

                        #  Delete the image from the Collection
                        Collection.unassign_image(image, collection)

                    #  Delete the image from the Database
                    image.delete()

                    responseMsg = 'Image Delete Success!'

                #  No ... 
                else:

                    #  Image Links have NOT been able to be deleted for this image!
                    responseMsg = 'Image Deletion NOT Allowed - Image Links NOT Deleted!'

            #  No
            else:

                #  Image Deletion is NOT allowed for NON WordPress/OMERO served Images
                responseMsg = 'Image Deletion NOT Allowed - Image Server is NOT OMERO or WordPress!'

        return Response(data=responseMsg)
