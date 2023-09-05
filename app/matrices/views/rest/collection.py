#!/usr/bin/python3
###!
# \file         collection.py
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
# The Collection View Set automatically provides `list`, `create`, `retrieve`,
# `update` and `destroy` actions.
###
from __future__ import unicode_literals

import subprocess

from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from matrices.models import Collection
from matrices.models import Artefact

from matrices.permissions import CollectionIsReadOnlyOrIsAdminOrIsOwner

from matrices.serializers import CollectionSerializer

from matrices.routines import exists_image_in_cells
from matrices.routines import exists_active_collection_for_user
from matrices.routines import exists_bench_for_last_used_collection
from matrices.routines import exists_user_for_last_used_collection
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_benches_for_last_used_collection
from matrices.routines import get_users_for_last_used_collection

#
# COLLECTION REST INTERFACE ROUTINES
#
class  CollectionViewSet(viewsets.ModelViewSet):
    """A ViewSet of Collections

    This viewset automatically provides:
        List, Create, Retrieve, Update and Destroy actions for Images.

    Parameters:
        None

    """


    queryset = Collection.objects.all()

    permission_classes = [ CollectionIsReadOnlyOrIsAdminOrIsOwner ]

    serializer_class = CollectionSerializer


    def list(self, request, *args, **kwargs):
        """List Collections.

        Listing Collections is NOT Allowed

        Parameters:

        Returns:

        Raises:
          
        """

        return Response(data='Collection LIST Not Available')


    def partial_update(self, request, *args, **kwargs):
        """Partial Update Collection.

        A Partial Update of a Collection is NOT Allowed

        Parameters:

        Returns:

        Raises:
          
        """

        return Response(data='Collection PARTIAL UPDATE Not Available')


    def destroy(self, request, *args, **kwargs):
        """Destroy Collection.

        This fucntion destroys the requested Collection.

        Parameters:

        Returns:

        Raises:
          
        """

        responseMsg = 'Collection  Deletion Response Message'

        boolAllowDelete = True

        collection = self.get_object()

        self.check_object_permissions(self.request, collection)

        # Get all the Images in the Collection
        image_list = collection.get_images()

        # Check each Image in the Collection
        for image in image_list:


            # Check if the Image is still referenced in a Cell
            #  Yes
            if exists_image_in_cells(image):

                boolAllowDelete = False
                
                #  Image Deletion is NOT allowed for Images still referenced in a Bench
                responseMsg = 'Collection Deletion NOT Allowed - Image still referenced in a Bench!'

            # No
            else:

                #  Get all the collections that have this Image
                list_collections = image.collections.all()

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
                                    artefact = get_object_or_404(Artefact, pk=image_link.artefact.id)

                                    # Does the Image Link have a file location
                                    if artefact.has_location():

                                        rm_command = 'rm ' + str(artefact.location)
                                        rm_escaped = rm_command.replace("(", "\(" ).replace(")", "\)" )
    
                                        # Delete the located file for this artefact
                                        process = subprocess.Popen(rm_escaped, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                                    # Delete the Image Link
                                    image_link.delete()

                                    # Delete the Artefact
                                    artefact.delete()

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
                                    artefact = get_object_or_404(Artefact, pk=image_link.artefact.id)

                                    # Does the Image Link have a file location
                                    if artefact.has_location():

                                        rm_command = 'rm ' + str(artefact.location)
                                        rm_escaped = rm_command.replace("(", "\(" ).replace(")", "\)" )

                                        # Delete the located file for this artefact
                                        process = subprocess.Popen(rm_escaped, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

                                    # Delete the Image Link
                                    image_link.delete()

                                    # Delete the Artefact
                                    artefact.delete()

                                else:

                                    # No, disallow the Image deletion
                                    boolAllowDelete = False

                    #  Can we delete this image ... ?
                    #  Yes ... 
                    if boolAllowDelete == True:

                        #  Process all the Collections that hold this image
                        for collection in list_collections:

                            #  Delete the image from the Collection
                            Collection.unassign_image(image, collection)

                        #  Delete the image from the Database
                        image.delete()

                        responseMsg = 'Image Delete Success!'
                
                    #  No ... 
                    else:

                        boolAllowDelete = False
                        
                        #  Image Links have NOT been able to be deleted for this image!
                        responseMsg = 'Collection Deletion NOT Allowed - Image Links NOT Deleted!'

                #  No
                else:

                    boolAllowDelete = False
                
                    #  Image Deletion is NOT allowed for NON WordPress/OMERO served Images
                    responseMsg = 'Collection Deletion NOT Allowed - Image Server is NOT OMERO or WordPress!'

        #  Can we delete this image ... ?
        #  Yes ... 
        if boolAllowDelete == True:

            # Has this Collection been Last Used in a Bench ... ?
            #  Yes
            if exists_bench_for_last_used_collection(collection):

                # Get all the Benches that last used this collection
                matrix_list = get_benches_for_last_used_collection(collection)

                # For each Bench that Last Used this Collection
                for matrix in matrix_list:

                    # Set the Bench to have NO Last Used Collection
                    matrix.set_no_last_used_collection()

                    # Update the Bench
                    matrix.save()


            # Has this Collection been Last Used by a User ... ?
            #  Yes
            if exists_user_for_last_used_collection(collection):

                # Get all the Users that last used this collection
                user_list = get_users_for_last_used_collection(collection)

                # For each User that Last Used this Collection
                for user in user_list:

                    # Set the User to have NO Last Used Collection
                    user.profile.set_last_used_collection(None)

                    # Update the User
                    user.save()


            # Is this Collection the User's Active Collection ... ?
            #  Yes
            if collection == get_active_collection_for_user(request.user):

                # Set the User to have NO Active Collection
                request.user.profile.set_active_collection(None)

                # Update the User
                request.user.save()


            # Does the User have an Active Collection ... ?
            #  Yes
            if exists_active_collection_for_user(request.user):

                # Get the Active Collection
                active_collection = get_active_collection_for_user(request.user)

                # Is this Collection the Active Collection ... ?
                #  Yes
                if active_collection == collection:

                    # CANNOT Delete this Collection!
                    responseMsg = 'Collection NOT Deleted - It is an Active Collection!'

                #  No
                else:
                
                    # Delete the Collection
                    collection.delete()
                    responseMsg = 'Collection Delete Success!'


            #  No
            else:

                # Delete the Collection
                collection.delete()
                responseMsg = 'Collection Delete Success!'


        return Response(data=responseMsg)

