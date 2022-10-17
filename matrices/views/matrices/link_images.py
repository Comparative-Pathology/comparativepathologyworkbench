#!/usr/bin/python3
###!
# \file		   link_images.py
# \author	   Mike Wicks
# \date		   March 2021
# \version	   $Id$
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
# This file contains the link_images view routine
#
###
from __future__ import unicode_literals

import os

from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from decouple import config

from matrices.forms import ArtefactForm

from matrices.models import Image
from matrices.models import Collection
from matrices.models import Artefact
from matrices.models import ImageLink

from matrices.routines import credential_exists
from matrices.routines import get_header_data

from matrices.routines import collection_list_by_user_and_direction
from matrices.routines import exists_active_collection_for_user
from matrices.routines import exists_image_in_image_list
from matrices.routines import exists_collection_in_collection_summary_list
from matrices.routines import get_images_for_collection
from matrices.routines import get_images_for_collection_summary
from matrices.routines import get_primary_cpw_server

HTTP_POST = 'POST'
WORDPRESS_SUCCESS = 'Success!'

#
# LINK_IMAGES VIEW ROUTINE
#
@login_required
def link_images(request, image_parent_id, image_child_id, collection_id):

    if request.is_ajax():

        raise PermissionDenied

    if not request.user.is_authenticated:

        raise PermissionDenied

    serverCPW = get_primary_cpw_server()

    if credential_exists(request.user):

        image_parent = None
        image_child = None
        selected_collection = None
        collection_image_list = list()

        image_list = list()

        collection_summary_list = collection_list_by_user_and_direction(request.user, '', '', '', '', '')

        image_list = get_images_for_collection_summary(collection_summary_list)

        if image_parent_id != 0:

            image_parent = get_object_or_404(Image, pk=image_parent_id)

            if not exists_image_in_image_list(image_parent, image_list):

                raise PermissionDenied

        if image_child_id != 0:

            image_child = get_object_or_404(Image, pk=image_child_id)

            if not exists_image_in_image_list(image_child, image_list):

                raise PermissionDenied

        if collection_id != 0:

            selected_collection = Collection.objects.get(id=collection_id)

            if not exists_collection_in_collection_summary_list(selected_collection, collection_summary_list):

                raise PermissionDenied

            collection_image_list = get_images_for_collection(selected_collection)


        if request.method == HTTP_POST:

            form = ArtefactForm(request.POST, request.FILES)

            if image_parent == None:

                messages.error(request, "CPW_WEB:0080 Link Images - No Parent Image Supplied!")
                form.add_error(None, "CPW_WEB:0080 Link Images - No Parent Image Supplied!")

            else:

                if image_child == None:

                    messages.error(request, "CPW_WEB:0080 Link Images - No Child Image Supplied!")
                    form.add_error(None, "CPW_WEB:0080 Link Images - No Child Image Supplied!")

                else:

                    if form.is_valid():

                        cd = form.cleaned_data

                        artefact = form.save(commit=False)

                        artefact.set_owner(request.user)

                        artefact.save()

                        if artefact.has_location():

                            location = str(artefact.location)

                            now = datetime.now()
                            date_time = now.strftime('%Y%m%d-%H:%M:%S.%f')[:-3]

                            initial_path = artefact.location.path
                            new_path = '/' + date_time + '_' + location
                            new_full_path = settings.MEDIA_ROOT + new_path

                            url = 'http://' + serverCPW.url_server + new_path

                            artefact.set_location(new_full_path)
                            artefact.set_url(url)

                            os.rename(initial_path, new_full_path)

                            artefact.save()

                        image_link = ImageLink.create(image_parent, image_child, artefact)

                        image_link.save()

                        return redirect('view_image_link', image_link_id=image_link.id)

                    else:

                        messages.error(request, "CPW_WEB:0080 Link Images - Form is Invalid!")
                        form.add_error(None, "CPW_WEB:0080 Link Images - Form is Invalid!")

        form = ArtefactForm()

        data = get_header_data(request.user)

        data.update({ 'form': form, 'image_parent': image_parent, 'image_child': image_child, 'selected_collection': selected_collection, 'collection_image_list': collection_image_list })

        return render(request, 'matrices/link_images.html', data)

    return HttpResponseRedirect(reverse('home', args=()))
