#!/usr/bin/python3
###!
# \file         matrix.py
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
# The Matrix View Set automatically provides `list`, `create`, `retrieve`,
# `update` and `destroy` actions.
###
from __future__ import unicode_literals

from django.db.models import Q

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from matrices.models import Matrix
from matrices.models import Cell

from matrices.permissions import MatrixIsReadOnlyOrIsAdminOrIsOwnerOrIsEditor

from matrices.serializers import MatrixSerializer

from matrices.routines import get_primary_wordpress_server
from matrices.routines import exists_collections_for_image
from matrices.routines import get_cells_for_image
from matrices.routines import get_credential_for_user


class MatrixViewSet(viewsets.ModelViewSet):
    """A ViewSet of Benches

    This viewset automatically provides:
        List, Create, Retrieve, Update and Destroy actions for Benches.

    Parameters:
        None

    """

    queryset = Matrix.objects.all()

    permission_classes = [ MatrixIsReadOnlyOrIsAdminOrIsOwnerOrIsEditor ]

    serializer_class = MatrixSerializer


    def list(self, request, *args, **kwargs):
        """List Images.

        Listing Benches is NOT Allowed

        Parameters:

        Returns:

        Raises:
          
        """

        return Response(data='Bench LIST Not Available')


    def partial_update(self, request, *args, **kwargs):
        """Partial Update Bench.

        A Partial Update of a Bench is NOT Allowed

        Parameters:

        Returns:

        Raises:
          
        """

        return Response(data='Bench PARTIAL UPDATE Not Available')


    def destroy(self, request, *args, **kwargs):
        """Destroy Bench.

        This fucntion destroys the requested Image.

        Parameters:

        Returns:

        Raises:
          
        """

        responseMsg = 'Bench Deletion Response Message'

        matrix = self.get_object()

        self.check_object_permissions(self.request, matrix)

        # Get All the Cells for this Bench
        cell_list = Cell.objects.filter(Q(matrix=matrix))

        credential = get_credential_for_user(request.user)

        serverWordpress = get_primary_wordpress_server()

        # Process All the cells in this Bench
        for cell in cell_list:

            # Does the Cell have a Blogpost ... ?
            #  Yes
            if cell.has_blogpost():

                # Does the User have a Blog Password ... ?
                #  Yes
                if credential.has_apppwd():

                    # Delete the Cell Blogpost
                    response = serverWordpress.delete_wordpress_post(credential, cell.blogpost)


            # Does the Cell have an Image ... ?
            #  Yes
            if cell.has_image():

                # Is the Image in a Collection ... ?
                #  No
                if not exists_collections_for_image(cell.image):

                    cell_list = get_cells_for_image(cell.image)

                    delete_flag = True

                    for otherCell in cell_list:

                        if otherCell.matrix.id != matrix.id:

                            delete_flag = False

                    if delete_flag == True:

                        image = cell.image

                        cell.image = None

                        cell.save()

                        image.delete()


        # Does the Bench have a Blogpost ... ?
        #  Yes
        if matrix.has_blogpost():

            # Does the User have a Blog Password ... ?
            #  Yes
            if credential.has_apppwd():

                # Delete the Bench Blogpost
                response = serverWordpress.delete_wordpress_post(credential, matrix.blogpost)

        responseMsg = 'Bench Delete Success!'

        # Delete the Bench!
        matrix.delete()

        return Response(data=responseMsg)
