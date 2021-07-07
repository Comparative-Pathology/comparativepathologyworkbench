#!/usr/bin/python3
###!
# \file         views_rest_matrix.py
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


from matrices.models import Collection
from matrices.models import Image

from matrices.permissions import CollectionIsReadOnlyOrIsAdminOrIsOwner

from matrices.serializers import CollectionSerializer

from matrices.routines import get_images_for_collection
from matrices.routines import get_collections_for_image
from matrices.routines import set_first_active_collection_for_user
from matrices.routines import exists_image_in_cells
from matrices.routines import exists_bench_for_last_used_collection
from matrices.routines import get_benches_for_last_used_collection

#
# COLLECTION REST INTERFACE ROUTINES
#
class  CollectionViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Collection.objects.all()

    permission_classes = [ CollectionIsReadOnlyOrIsAdminOrIsOwner ]

    serializer_class = CollectionSerializer


    def list(self, request, *args, **kwargs):

        return Response(data='Collection LIST Not Available')


    def partial_update(self, request, *args, **kwargs):

        return Response(data='Collection PARTIAL UPDATE Not Available')



    def destroy(self, request, *args, **kwargs):

        collection = self.get_object()

        self.check_object_permissions(self.request, collection)

        image_list = get_images_for_collection(collection)

        for image in image_list:

            collection_list = get_collections_for_image(image)

            delete_flag = False

            for collection_other in collection_list:

                if collection != collection_other:

                    delete_flag = True

            if delete_flag == False:

                if not exists_image_in_cells(image):

                    image.delete()


        if exists_bench_for_last_used_collection(collection):

            matrix_list = get_benches_for_last_used_collection(collection)

            for matrix in matrix_list:

                matrix.set_no_last_used_collection()

                matrix.save()


        if collection.is_active():

            set_first_active_collection_for_user(request.user)


        collection.delete()

        return Response(data='Collection Delete Success')
