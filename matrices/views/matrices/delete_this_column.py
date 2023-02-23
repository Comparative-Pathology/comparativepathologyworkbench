#!/usr/bin/python3
###!
# \file         delete_this_column.py
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
# This file contains the delete_this_column view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from matrices.models import Matrix
from matrices.models import Cell

from matrices.routines import credential_exists
from matrices.routines import exists_collections_for_image
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import get_cells_for_image
from matrices.routines import get_credential_for_user
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_header_data


#
# DELETE THE GIVEN COLUMN IN THE BENCH
#
@login_required
def delete_this_column(request, matrix_id, column_id):

    serverWordpress = get_primary_wordpress_server()

    data = get_header_data(request.user)

    if credential_exists(request.user):

        matrix = get_object_or_404(Matrix, pk=matrix_id)

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() == True or authority.is_none() == True:

            return HttpResponseRedirect(reverse('home', args=()))

        else:

            matrix = Matrix.objects.get(id=matrix_id)

            deleteColumn = int(column_id)

            oldCells = Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn)

            for oldCell in oldCells:

                if oldCell.has_blogpost() == True:

                    credential = get_credential_for_user(request.user)

                    if credential.has_apppwd():

                        response = serverWordpress.delete_wordpress_post(credential, oldCell.blogpost)


                if oldCell.has_image():

                    if exists_collections_for_image(oldCell.image):
                                       
                        cell_list = get_cells_for_image(oldCell.image)
                    
                        other_bench_Flag = False
                    
                        for otherCell in cell_list:
                        
                            if otherCell.matrix.id != matrix.id:
                            
                                other_bench_Flag = True
                            
                        if other_bench_Flag == True:
                          
                            if request.user.profile.is_hide_collection_image():
                                
                                oldCell.image.set_hidden(True)
                                oldCell.image.save()
                                
                            else:
                                
                                oldCell.image.set_hidden(False)
                                oldCell.image.save()
                        
                        else:
                            
                            oldCell.image.set_hidden(False)
                            oldCell.image.save()
                            
                    else:

                        cell_list = get_cells_for_image(oldCell.image)

                        delete_flag = True

                        for otherCell in cell_list:

                            if otherCell.matrix.id != matrix_id:

                                delete_flag = False

                        if delete_flag == True:

                            image = oldCell.image

                            oldCell.image = None

                            oldCell.save()

                            image.delete()


            Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn).delete()

            moveCells = Cell.objects.filter(matrix=matrix_id, xcoordinate__gt=deleteColumn)

            for moveCell in moveCells:

                moveCell.decrement_x()

                moveCell.save()

            matrix.save()

            matrix_cells = matrix.get_matrix()
            columns = matrix.get_columns()
            rows = matrix.get_rows()

            data.update({ 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells })

            return HttpResponseRedirect(reverse('matrix', args=(matrix_id,)))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
