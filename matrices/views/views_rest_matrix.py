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

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Image
from matrices.models import Credential

from matrices.permissions import MatrixIsReadOnlyOrIsAdminOrIsOwnerOrIsEditor

from matrices.serializers import MatrixSerializer

from matrices.routines import get_primary_wordpress_server
from matrices.routines import exists_collections_for_image
from matrices.routines import get_cells_for_image


WORDPRESS_SUCCESS = 'Success!'


#
# BENCH REST INTERFACE ROUTINES
#
class MatrixViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Matrix.objects.all()
    
    permission_classes = [ MatrixIsReadOnlyOrIsAdminOrIsOwnerOrIsEditor ]

    serializer_class = MatrixSerializer


    def list(self, request, *args, **kwargs):

        return Response(data='Bench LIST Not Available')


    def partial_update(self, request, *args, **kwargs):

        return Response(data='Bench PARTIAL UPDATE Not Available')


    def destroy(self, request, *args, **kwargs):

        matrix = self.get_object()

        self.check_object_permissions(self.request, matrix) 

        cell_list = Cell.objects.filter(Q(matrix=matrix))
        
        credential = Credential.objects.get(username=request.user.username)
        
        serverWordpress = get_primary_wordpress_server()
        
        for cell in cell_list:
                
            if cell.has_blogpost():
                
                if credential.has_apppwd():
                
                    serverWordpress = get_primary_wordpress_server()
                
                    response = serverWordpress.delete_wordpress_post(request.user.username, cell.blogpost)
                    
                    if response != WORDPRESS_SUCCESS:
                    
                        messages.error(request, "WordPress Error - Contact System Administrator")
                        
            if cell.has_image():
                
                if not exists_collections_for_image(cell.image):
                    
                    cell_list = get_cells_for_image(cell.image)
                        
                    delete_flag = True
                        
                    for otherCell in cell_list:
                        
                        if otherCell.matrix.id != matrix_id:
                            
                            delete_flag = False
                        
                        if delete_flag == True:
                        
                            image = cell.image
                            
                            cell.image = None
                            
                            cell.save()
                            
                            image.delete()

            cell.delete()
        
        if matrix.has_blogpost():

            if credential.has_apppwd():

                response = serverWordpress.delete_wordpress_post(request.user.username, matrix.blogpost)

                if response != WORDPRESS_SUCCESS:
                    
                    messages.error(request, "WordPress Error - Contact System Administrator")

        matrix.delete()

        return Response(data='Bench Delete Success')

