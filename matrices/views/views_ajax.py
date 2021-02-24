from __future__ import unicode_literals

import os
import time
import requests

from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages 
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.db.models import Q 

from decouple import config


from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Type
from matrices.models import Protocol
from matrices.models import Server
from matrices.models import Command
from matrices.models import Image
from matrices.models import Blog
from matrices.models import Credential
from matrices.models import Collection
from matrices.models import Authority
from matrices.models import CollectionAuthority
from matrices.models import Authorisation
from matrices.models import CollectionAuthorisation

from matrices.routines import credential_exists
from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_authority_for_bench_and_user_and_requester
from matrices.routines import exists_collections_for_image
from matrices.routines import get_cells_for_image


WORDPRESS_SUCCESS = 'Success!'


#
# AJAX INTERFACE ROUTINES
#
# def overwrite_cell(request) - MOVE
# def overwrite_cell_leave(request) - COPY
# def swap_cells(request) - SWAP
# def import_image(request)
# def swap_rows(request) - SWAP ROW A WITH ROW B
# def swap_columns(request) - SWAP COLUMN A WITH COLUMN B
# def shuffle_columns(request) - MOVE COLUMN AND PUSH EXISTING COLUMNS TO LEFT OR RIGHT
# def shuffle_rows(request) - MOVE ROW AND PUSH EXISTING ROWS TO LEFT OR RIGHT
#

#
# OVERWRITE A CELL - MOVE
#
@login_required()
def overwrite_cell(request):
    """
    AJAX - Overwrite Cell - MOVE
    """

    source = request.POST['source']
    target = request.POST['target']
    source_type = request.POST['source_type']

    source_cell = get_object_or_404(Cell, pk=source)
    target_cell = get_object_or_404(Cell, pk=target)
    
    matrix = source_cell.matrix
    
    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    serverWordpress = get_primary_wordpress_server()

    if credential_exists(user):

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():
        
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)
    
        else:

            if matrix.get_max_row() == target_cell.ycoordinate:

                nextRow = matrix.get_row_count()
                columns = matrix.get_columns()

                for i, column in enumerate(columns):
                
                    cell = Cell.create(matrix, "", "", i, nextRow, "", None)
                    
                    cell.save()

                matrix.save()

            if matrix.get_max_column() == target_cell.xcoordinate:
    
                nextColumn = matrix.get_column_count()
                rows = matrix.get_rows()
    
                for i, row in enumerate(rows):

                    cell = Cell.create(matrix, "", "", nextColumn, i, "", None)

                    cell.save()

                matrix.save()

            if target_cell.has_blogpost():

                credential = Credential.objects.get(username=request.user.username)
    
                if credential.has_apppwd():
            
                    response = serverWordpress.delete_wordpress_post(request.user.username, target_cell.blogpost)

                    if response != WORDPRESS_SUCCESS:
                    
                        messages.error(request, "WordPress Error - Contact System Administrator")
                        
            if target_cell.has_image():
            
                if not exists_collections_for_image(target_cell.image):
                    
                    cell_list = get_cells_for_image(target_cell.image)
                        
                    delete_flag = True
                        
                    for otherCell in cell_list:
                        
                        if otherCell.matrix.id != matrix_id:
                            
                            delete_flag = False
                        
                    if delete_flag == True:
                        
                        image = target_cell.image
                            
                        target_cell.image = None
                            
                        target_cell.save()
                            
                        image.delete()


            source_xcoordinate = source_cell.xcoordinate
            source_ycoordinate = source_cell.ycoordinate

            target_xcoordinate = target_cell.xcoordinate
            target_ycoordinate = target_cell.ycoordinate
    
            source_cell.xcoordinate = target_xcoordinate
            source_cell.ycoordinate = target_ycoordinate

            target_cell.xcoordinate = source_xcoordinate
            target_cell.ycoordinate = source_ycoordinate

            target_cell.title = ""
            target_cell.description = ""

            target_cell.blogpost = ""
            target_cell.image = None
            
            source_cell.save()
            target_cell.save()

            data = { 'failure': False, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)

    else:
    
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)


#
# OVERWRITE A TARGET CELL AND LEAVE SOURCE IN PLACE - COPY
#
@login_required()
def overwrite_cell_leave(request):
    """
    AJAX - Overwrite Cell
    """

    source = request.POST['source']
    target = request.POST['target']
    source_type = request.POST['source_type']
    
    source_cell = get_object_or_404(Cell, pk=source)
    target_cell = get_object_or_404(Cell, pk=target)
    
    matrix = source_cell.matrix
    
    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    serverWordpress = get_primary_wordpress_server()

    if credential_exists(user):

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():
        
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)
    
        else:

            if matrix.get_max_row() == target_cell.ycoordinate:

                nextRow = matrix.get_row_count()
                columns = matrix.get_columns()

                for i, column in enumerate(columns):

                    cell = Cell.create(matrix, "", "", i, nextRow, "", None)

                    cell.save()

                matrix.save()

            if matrix.get_max_column() == target_cell.xcoordinate:
    
                nextColumn = matrix.get_column_count()
                rows = matrix.get_rows()
    
                for i, row in enumerate(rows):

                    cell = Cell.create(matrix, "", "", nextColumn, i, "", None)

                    cell.save()

                matrix.save()

            if target_cell.has_blogpost():

                credential = Credential.objects.get(username=request.user.username)
    
                if credential.has_apppwd():
            
                    response = serverWordpress.delete_wordpress_post(request.user.username, target_cell.blogpost)

                    if response != WORDPRESS_SUCCESS:
                    
                        messages.error(request, "WordPress Error - Contact System Administrator")

            if target_cell.has_image():
            
                if not exists_collections_for_image(target_cell.image):
                    
                    cell_list = get_cells_for_image(target_cell.image)
                        
                    delete_flag = True
                        
                    for otherCell in cell_list:
                        
                        if otherCell.matrix.id != matrix_id:
                            
                            delete_flag = False
                        
                    if delete_flag == True:
                        
                        image = target_cell.image
                            
                        target_cell.image = None
                            
                        target_cell.save()
                            
                        image.delete()

            target_cell.title = source_cell.title
            target_cell.description = source_cell.description
            
            if source_cell.has_image():
            
                imageOld = Image.objects.get(pk=source_cell.image.id)

                imageNew = Image.create(imageOld.identifier, imageOld.name, imageOld.server, imageOld.viewer_url, imageOld.birdseye_url, imageOld.roi, imageOld.owner)

                imageNew.save()
                
                target_cell.image = imageNew

            
            target_cell.blogpost = source_cell.blogpost

            if source_cell.has_blogpost():
                
                credential = Credential.objects.get(username=request.user.username)
    
                post_id = ''

                if credential.has_apppwd():

                    returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, source_cell.title, source_cell.description)
                                
                    if returned_blogpost['status'] == WORDPRESS_SUCCESS:
                                
                        post_id = returned_blogpost['id']

                    else:
                                
                        messages.error(request, "WordPress Error - Contact System Administrator")
                            
                source_cell.set_blogpost(post_id)


            source_cell.save()
            target_cell.save()

            data = { 'failure': False, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)

    else:
    
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)


#
# SWAP TARGET AND SOURCE CELLS - SWAP
#
@login_required()
def swap_cells(request):
    """
    AJAX - Swap Cells
    """

    source = request.POST['source']
    target = request.POST['target']
    source_type = request.POST['source_type']
    
    source_cell = get_object_or_404(Cell, pk=source)
    target_cell = get_object_or_404(Cell, pk=target)
    
    matrix = source_cell.matrix
    
    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    if credential_exists(user):

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():
        
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)
    
        else:

            if matrix.get_max_row() == target_cell.ycoordinate:

                nextRow = matrix.get_row_count()
                columns = matrix.get_columns()

                for i, column in enumerate(columns):

                    cell = Cell.create(matrix, "", "", i, nextRow, "", None)

                    cell.save()

                matrix.save()

            if matrix.get_max_column() == target_cell.xcoordinate:
    
                nextColumn = matrix.get_column_count()
                rows = matrix.get_rows()
    
                for i, row in enumerate(rows):

                    cell = Cell.create(matrix, "", "", nextColumn, i, "", None)

                    cell.save()

                matrix.save()


            source_xcoordinate = source_cell.xcoordinate
            source_ycoordinate = source_cell.ycoordinate

            target_xcoordinate = target_cell.xcoordinate
            target_ycoordinate = target_cell.ycoordinate
    
            source_cell.xcoordinate = target_xcoordinate
            source_cell.ycoordinate = target_ycoordinate

            target_cell.xcoordinate = source_xcoordinate
            target_cell.ycoordinate = source_ycoordinate

            source_cell.save()
            target_cell.save()


            data = { 'failure': False, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)

    else:
    
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)


#
# IMPORT AN IMAGE FROM BASKET TO CELL - IMPORT
#
@login_required()
def import_image(request):
    """
    AJAX - Import Image
    """

    source = request.POST['source']
    target = request.POST['target']
    source_type = request.POST['source_type']
    
    source_image = get_object_or_404(Image, pk=source)
    target_cell = get_object_or_404(Cell, pk=target)
    
    matrix = target_cell.matrix
    
    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    serverWordpress = get_primary_wordpress_server()

    if credential_exists(user):

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():
        
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)
    
        else:

            if matrix.get_max_row() == target_cell.ycoordinate:

                nextRow = matrix.get_row_count()
                columns = matrix.get_columns()

                for i, column in enumerate(columns):

                    cell = Cell.create(matrix, "", "", i, nextRow, "", None)

                    cell.save()

                matrix.save()

            if matrix.get_max_column() == target_cell.xcoordinate:
    
                nextColumn = matrix.get_column_count()
                rows = matrix.get_rows()
    
                for i, row in enumerate(rows):

                    cell = Cell.create(matrix, "", "", nextColumn, i, "", None)

                    cell.save()

                matrix.save()

            post_id = ''
                
            target_cell.title = source_image.name
            target_cell.description = source_image.name
            
            target_cell.image = source_image
            
            if target_cell.has_no_blogpost():
                
                credential = Credential.objects.get(username=request.user.username)
    
                if credential.has_apppwd():

                    returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, target_cell.title, target_cell.description)
                                
                    if returned_blogpost['status'] == WORDPRESS_SUCCESS:
                                
                        post_id = returned_blogpost['id']

                    else:
                                
                        messages.error(request, "WordPress Error - Contact System Administrator")
                                
                target_cell.set_blogpost(post_id)

            target_cell.save()


            data = { 'failure': False, 'source': str(source), 'target': str(target) }
            
            return JsonResponse(data)

    else:
    
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)


#
# SWAP ROWS - SWAP ROW A WITH ROW B
#
@login_required()
def swap_rows(request):
    """
    AJAX - Swap Rows
    """

    source = request.POST['source']
    target = request.POST['target']
        
    in_source_cell = get_object_or_404(Cell, pk=source)
    in_target_cell = get_object_or_404(Cell, pk=target)
    
    matrix = in_source_cell.matrix

    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    if credential_exists(user):

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():
        
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)
    
        else:

            source_row_cells = matrix.get_row(in_source_cell.ycoordinate)
            target_row_cells = matrix.get_row(in_target_cell.ycoordinate)
    
            source_ycoordinate = in_source_cell.ycoordinate
            target_ycoordinate = in_target_cell.ycoordinate
    
            output_cells = list()
    
            for target_cell in target_row_cells:
    
                target_cell.set_ycoordinate(source_ycoordinate)
    
                output_cells.append(target_cell)
    
            for source_cell in source_row_cells:
    
                source_cell.set_ycoordinate(target_ycoordinate)
    
                output_cells.append(source_cell)

            for output_cell in output_cells:

                output_cell.save()
        

            if matrix.get_max_row() == in_target_cell.ycoordinate:

                nextRow = matrix.get_row_count()
                columns = matrix.get_columns()

                for i, column in enumerate(columns):

                    cell = Cell.create(matrix, "", "", i, nextRow, "", None)

                    cell.save()

                matrix.save()

    
            data = { 'failure': False, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)

    else:
    
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)


#
# SWAP COLUMNS - SWAP COLUMN A WITH COLUMN B
#
@login_required()
def swap_columns(request):
    """
    AJAX - Swap Columns
    """

    source = request.POST['source']
    target = request.POST['target']
        
    in_source_cell = get_object_or_404(Cell, pk=source)
    in_target_cell = get_object_or_404(Cell, pk=target)
    
    matrix = in_source_cell.matrix

    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    if credential_exists(user):

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():
        
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)
    
        else:

            source_column_cells = matrix.get_column(in_source_cell.xcoordinate)
            target_column_cells = matrix.get_column(in_target_cell.xcoordinate)
    
            source_xcoordinate = in_source_cell.xcoordinate
            target_xcoordinate = in_target_cell.xcoordinate
    
            output_cells = list()
    
            for target_cell in target_column_cells:
    
                target_cell.set_xcoordinate(source_xcoordinate)
    
                output_cells.append(target_cell)
    
            for source_cell in source_column_cells:
    
                source_cell.set_xcoordinate(target_xcoordinate)
    
                output_cells.append(source_cell)

            for output_cell in output_cells:

                output_cell.save()
    

            if matrix.get_max_column() == in_target_cell.xcoordinate:
    
                nextColumn = matrix.get_column_count()
                rows = matrix.get_rows()
    
                for i, row in enumerate(rows):

                    cell = Cell.create(matrix, "", "", nextColumn, i, "", None)

                    cell.save()

                matrix.save()

    
            data = { 'failure': False, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)    

    else:
    
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)


#
# SHUFFLE COLUMNS - MOVE COLUMN AND PUSH EXISTING COLUMNS TO LEFT OR RIGHT
#
@login_required()
def shuffle_columns(request):
    """
    AJAX - Shuffle Columns
    """

    source = request.POST['source']
    target = request.POST['target']
        
    in_source_cell = get_object_or_404(Cell, pk=source)
    in_target_cell = get_object_or_404(Cell, pk=target)
    
    source_xcoordinate = in_source_cell.xcoordinate
    target_xcoordinate = in_target_cell.xcoordinate
    
    matrix = in_source_cell.matrix

    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    if credential_exists(user):

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():
        
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)
    
        else:

            source_column_cells = matrix.get_column(source_xcoordinate)

            if source_xcoordinate < target_xcoordinate:
            
                oldCells = Cell.objects.filter(matrix=matrix.id).filter(xcoordinate__gt=source_xcoordinate).filter(xcoordinate__lte=target_xcoordinate)

                output_cells = list()
    
                for oldcell in oldCells:
        
                    oldcell.decrement_x()
                
                    output_cells.append(oldcell)
                
                for source_cell in source_column_cells:
    
                    source_cell.set_xcoordinate(target_xcoordinate)
    
                    output_cells.append(source_cell)
            
                for output_cell in output_cells:
            
                    output_cell.save()


            if source_xcoordinate > target_xcoordinate:

                oldCells = Cell.objects.filter(matrix=matrix.id).filter(xcoordinate__gte=target_xcoordinate).filter(xcoordinate__lt=source_xcoordinate)

                output_cells = list()
    
                for oldcell in oldCells:
        
                    oldcell.increment_x()
                
                    output_cells.append(oldcell)
                
                for source_cell in source_column_cells:
    
                    source_cell.set_xcoordinate(target_xcoordinate)
    
                    output_cells.append(source_cell)
            
                for output_cell in output_cells:
            
                    output_cell.save()


            if matrix.get_max_column() == target_xcoordinate:
    
                nextColumn = matrix.get_column_count()
                rows = matrix.get_rows()
    
                for i, row in enumerate(rows):

                    cell = Cell.create(matrix, "", "", nextColumn, i, "", None)

                    cell.save()

                matrix.save()

    
            data = { 'failure': False, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)    
    
    else:
    
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)


#
# SHUFFLE ROWS - MOVE ROW AND PUSH EXISTING ROWS TO LEFT OR RIGHT
#
@login_required()
def shuffle_rows(request):
    """
    AJAX - Shuffle the Rows
    """

    source = request.POST['source']
    target = request.POST['target']
        
    in_source_cell = get_object_or_404(Cell, pk=source)
    in_target_cell = get_object_or_404(Cell, pk=target)
    
    source_ycoordinate = in_source_cell.ycoordinate
    target_ycoordinate = in_target_cell.ycoordinate

    matrix = in_source_cell.matrix

    owner = get_object_or_404(User, pk=matrix.owner_id)
    user = get_object_or_404(User, pk=request.user.id)

    if credential_exists(user):

        authority = get_authority_for_bench_and_user_and_requester(matrix, request.user)

        if authority.is_viewer() or authority.is_none():
        
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)
    
        else:

            source_row_cells = matrix.get_row(source_ycoordinate)
            
            if source_ycoordinate < target_ycoordinate:
            
                oldCells = Cell.objects.filter(matrix=matrix.id).filter(ycoordinate__gt=source_ycoordinate).filter(ycoordinate__lte=target_ycoordinate)

                output_cells = list()
    
                for oldcell in oldCells:
        
                    oldcell.decrement_y()
                
                    output_cells.append(oldcell)
                
                for source_cell in source_row_cells:
    
                    source_cell.set_ycoordinate(target_ycoordinate)
    
                    output_cells.append(source_cell)
            
                for output_cell in output_cells:
            
                    output_cell.save()


            if source_ycoordinate > target_ycoordinate:

                oldCells = Cell.objects.filter(matrix=matrix.id).filter(ycoordinate__gte=target_ycoordinate).filter(ycoordinate__lt=source_ycoordinate)

                output_cells = list()
    
                for oldcell in oldCells:
        
                    oldcell.increment_y()
                
                    output_cells.append(oldcell)
                
                for source_cell in source_row_cells:
    
                    source_cell.set_ycoordinate(target_ycoordinate)
    
                    output_cells.append(source_cell)
            
                for output_cell in output_cells:
            
                    output_cell.save()


            if matrix.get_max_row() == target_ycoordinate:

                nextRow = matrix.get_row_count()
                columns = matrix.get_columns()

                for i, column in enumerate(columns):

                    cell = Cell.create(matrix, "", "", i, nextRow, "", None)

                    cell.save()

                matrix.save()

    
            data = { 'failure': False, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)
    
    else:
    
            data = { 'failure': True, 'source': str(source), 'target': str(target) }
    
            return JsonResponse(data)

