#!/usr/bin/python3
#
# ##
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
# ##
#
from __future__ import unicode_literals

from django.db.models import Q

from rest_framework import viewsets
from rest_framework.response import Response

from matrices.models import Cell
from matrices.models import Credential
from matrices.models import Matrix

from matrices.permissions import MatrixIsReadOnlyOrIsAdminOrIsOwnerOrIsEditor

from matrices.serializers import MatrixSerializer

from matrices.routines import bench_list_by_user_and_direction
from matrices.routines import exists_collections_for_image
from matrices.routines import get_cells_for_image
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment


class MatrixViewSet(viewsets.ModelViewSet):
    """A ViewSet of Benches

    This viewset automatically provides:
        List, Create, Retrieve, Update and Destroy actions for Benches.

    Parameters:
        None

    """

    queryset = Matrix.objects.all()

    permission_classes = [MatrixIsReadOnlyOrIsAdminOrIsOwnerOrIsEditor]

    serializer_class = MatrixSerializer

    def get_queryset(self):

        query_title = self.request.query_params.get('title', '')
        query_description = self.request.query_params.get('description', '')
        query_owner = self.request.query_params.get('owner', '')
        query_authority = ''
        query_created_before = self.request.query_params.get('created_before', '')
        query_created_after = self.request.query_params.get('created_after', '')
        query_modified_before = self.request.query_params.get('modified_before', '')
        query_modified_after = self.request.query_params.get('modified_after', '')

        query_search = ''

        sort_parameter = 'matrix_id'
        order_parameter = 'matrix_id'
        order_parameter_2 = 'id'

        if self.request.query_params.get('sort', None) is None:

            sort_parameter = 'matrix_id'

        else:

            sort_parameter = self.request.query_params.get('sort', None)

        if sort_parameter == 'id':
            order_parameter = 'matrix_id'
            order_parameter_2 = 'id'

        if sort_parameter == '-id':
            order_parameter = '-matrix_id'
            order_parameter_2 = '-id'

        if sort_parameter == 'title':
            order_parameter = 'matrix_title'
            order_parameter_2 = 'title'

        if sort_parameter == '-title':
            order_parameter = '-matrix_title'
            order_parameter_2 = '-title'

        if sort_parameter == 'created':
            order_parameter = 'matrix_created'
            order_parameter_2 = 'created'

        if sort_parameter == '-created':
            order_parameter = '-matrix_created'
            order_parameter_2 = '-created'

        if sort_parameter == 'updated':
            order_parameter = 'matrix_updated'
            order_parameter_2 = 'updated'

        if sort_parameter == '-updated':
            order_parameter = '-matrix_updated'
            order_parameter_2 = '-updated'

        if sort_parameter == 'owner':
            order_parameter = 'matrix_owner'
            order_parameter_2 = 'owner'

        if sort_parameter == '-owner':
            order_parameter = '-matrix_owner'
            order_parameter_2 = '-owner'

        if sort_parameter == 'matrix_id':
            order_parameter = 'matrix_id'
            order_parameter_2 = 'id'

        if sort_parameter == '-matrix_id':
            order_parameter = '-matrix_id'
            order_parameter_2 = '-id'

        if sort_parameter == 'matrix_title':
            order_parameter = 'matrix_title'
            order_parameter_2 = 'title'

        if sort_parameter == '-matrix_title':
            order_parameter = '-matrix_title'
            order_parameter_2 = '-title'

        if sort_parameter == 'matrix_created':
            order_parameter = 'matrix_created'
            order_parameter_2 = 'created'

        if sort_parameter == '-matrix_created':
            order_parameter = '-matrix_created'
            order_parameter_2 = '-created'

        if sort_parameter == 'matrix_updated':
            order_parameter = 'matrix_updated'
            order_parameter_2 = 'updated'

        if sort_parameter == '-matrix_updated':
            order_parameter = '-matrix_updated'
            order_parameter_2 = '-updated'

        if sort_parameter == 'matrix_owner':
            order_parameter = 'matrix_owner'
            order_parameter_2 = 'owner'

        if sort_parameter == '-matrix_owner':
            order_parameter = '-matrix_owner'
            order_parameter_2 = '-owner'

        if sort_parameter != 'id' and \
           sort_parameter != '-id' and \
           sort_parameter != 'title' and \
           sort_parameter != '-title' and \
           sort_parameter != 'created' and \
           sort_parameter != '-created' and \
           sort_parameter != 'updated' and \
           sort_parameter != '-updated' and \
           sort_parameter != 'owner' and \
           sort_parameter != '-owner' and \
           sort_parameter != 'matrix_id' and \
           sort_parameter != '-matrix_id' and \
           sort_parameter != 'matrix_title' and \
           sort_parameter != '-matrix_title' and \
           sort_parameter != 'matrix_created' and \
           sort_parameter != '-matrix_created' and \
           sort_parameter != 'matrix_updated' and \
           sort_parameter != '-matrix_updated' and \
           sort_parameter != 'matrix_owner' and \
           sort_parameter != '-matrix_owner':

            order_parameter = 'matrix_id'
            order_parameter_2 = 'id'

        bench_summary_queryset = bench_list_by_user_and_direction(self.request.user,
                                                                  order_parameter,
                                                                  query_title,
                                                                  query_description,
                                                                  query_owner,
                                                                  query_authority,
                                                                  query_created_after,
                                                                  query_created_before,
                                                                  query_modified_after,
                                                                  query_modified_before,
                                                                  query_search)

        bench_queryset = Matrix.objects.none()

        list_of_bench_ids = []

        for bench_summary in bench_summary_queryset:

            list_of_bench_ids.append(bench_summary.matrix_id)

        bench_queryset = Matrix.objects.filter(id__in=list_of_bench_ids).order_by(order_parameter_2)

        return bench_queryset

    def list(self, request, *args, **kwargs):
        """List Images.

        Listing Benches is NOT Allowed

        Parameters:

        Returns:

        Raises:

        """

        responseMsg = 'Bench List Response Message'

        query_title = self.request.query_params.get('title', '')
        query_description = self.request.query_params.get('description', '')
        query_owner = self.request.query_params.get('owner', '')
        query_authority = self.request.query_params.get('authority', '')
        query_created_before = self.request.query_params.get('created_before', '')
        query_created_after = self.request.query_params.get('created_after', '')
        query_modified_before = self.request.query_params.get('modified_before', '')
        query_modified_after = self.request.query_params.get('modified_after', '')

        if not request.user.is_superuser:

            if query_title == "" and \
               query_description == "" and \
               query_owner == "" and \
               query_authority == "" and \
               query_created_before == "" and \
               query_created_after == "" and \
               query_modified_before == "" and \
               query_modified_after == "":

                responseMsg = 'Bench LIST Not Available without Search Parameters!'

                return Response(data=responseMsg)

        queryset = self.get_queryset()

        serializer = MatrixSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)

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

        credential = Credential.objects.get_or_none(username=request.user.username)

        environment = get_primary_cpw_environment()

        # Process All the cells in this Bench
        for cell in cell_list:

            # Does the Cell have a Blogpost ... ?
            #  Yes
            if cell.has_blogpost():

                # Does the User have a Blog Password ... ?
                #  Yes
                if credential.has_apppwd() and environment.is_wordpress_active():

                    # Delete the Cell Blogpost
                    response = environment.delete_a_post_from_wordpress(credential, cell.blogpost)

            # Does the Cell have an Image ... ?
            #  Yes
            if cell.has_image():

                # Is the Image in a Collection ... ?
                #  No
                if exists_collections_for_image(cell.image):

                    cell_list = get_cells_for_image(cell.image)

                    other_bench_Flag = False

                    for otherCell in cell_list:

                        if otherCell.matrix.id != matrix.id:

                            other_bench_Flag = True

                    if other_bench_Flag is True:

                        if request.user.profile.is_hide_collection_image():

                            cell.image.set_hidden(True)
                            cell.image.save()

                        else:

                            cell.image.set_hidden(False)
                            cell.image.save()

                    else:

                        cell.image.set_hidden(False)
                        cell.image.save()

                else:

                    cell_list = get_cells_for_image(cell.image)

                    delete_flag = True

                    for otherCell in cell_list:

                        if otherCell.matrix.id != matrix.id:

                            delete_flag = False

                    if delete_flag is True:

                        image = cell.image

                        cell.image = None

                        cell.save()

                        image.delete()

        # Does the Bench have a Blogpost ... ?
        #  Yes
        if matrix.has_blogpost():

            # Does the User have a Blog Password ... ?
            #  Yes
            if credential.has_apppwd() and environment.is_wordpress_active():

                # Delete the Bench Blogpost
                response = environment.delete_a_post_from_wordpress(credential, matrix.blogpost)

        responseMsg = 'Bench Delete Success!'

        # Delete the Bench!
        matrix.delete()

        return Response(data=responseMsg)
