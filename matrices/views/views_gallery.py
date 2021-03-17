#!/usr/bin/python3
###!
# \file         views_gallery.py
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
# This contains the show_imaging_server, show_group, show_project, show_dataset,
# show_image, show_wordpress, show_wordpress_image and add_image views
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


from matrices.models import Server
from matrices.models import Image
from matrices.models import Collection

from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import get_image_count_for_image


NO_CREDENTIALS = ''


#
# GALLERY VIEW ROUTINES
#
# def show_imaging_server(request, server_id):
# def show_group(request, server_id, group_id):
# def show_project(request, server_id, project_id):
# def show_dataset(request, server_id, dataset_id):
# def show_image(request, server_id, image_id):
# def show_wordpress(request, server_id, page_id):
# def show_wordpress_image(request, server_id, image_id):
# def add_image(request, server_id, image_id, roi_id):
#

#
# SHOW THE AVAILABLE GROUPS
#  FROM AN OMERO IMAGING SERVER
#
@login_required()
def show_imaging_server(request, server_id):
    """
    Show the Imaging Server
    """

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if server.is_omero547() or server.is_omero56():

            server_data = server.get_imaging_server_json(request)

            data.update(server_data)

            return render(request, 'gallery/show_server.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))


#
# SHOW THE AVAILABLE PROJECTS
#  WITHIN THE AVAILABLE GROUPS
#   FROM AN OMERO IMAGING SERVER
#
@login_required()
def show_group(request, server_id, group_id):
    """
    Show a group
    """

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if server.is_omero547() or server.is_omero56():

            server_data = server.get_imaging_server_group_json(request, group_id)

            data.update(server_data)

            return render(request, 'gallery/show_group.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))


#
# SHOW THE AVAILABLE DATASETS
#  WITHIN THE AVAILABLE PROJECTS
#  WITHIN THE AVAILABLE GROUPS
#   FROM AN OMERO IMAGING SERVER
#
@login_required()
def show_project(request, server_id, project_id):
    """
    Show a project
    """

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if server.is_omero547() or server.is_omero56():

            server_data = server.get_imaging_server_project_json(request, project_id)

            data.update(server_data)

            return render(request, 'gallery/show_project.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))


#
# SHOW THE AVAILABLE IMAGES
#  WITHIN THE AVAILABLE DATASETS
#  WITHIN THE AVAILABLE PROJECTS
#  WITHIN THE AVAILABLE GROUPS
#   FROM AN OMERO IMAGING SERVER
#
@login_required()
def show_dataset(request, server_id, dataset_id):
    """
    Show a dataset
    """

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if server.is_omero547() or server.is_omero56():

            server_data = server.get_imaging_server_dataset_json(request, dataset_id)

            data.update(server_data)

            return render(request, 'gallery/show_dataset.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))


#
# SHOW THE IMAGE
#  WITHIN THE AVAILABLE IMAGES
#  WITHIN THE AVAILABLE DATASETS
#  WITHIN THE AVAILABLE PROJECTS
#  WITHIN THE AVAILABLE GROUPS
#   FROM AN OMERO IMAGING SERVER
#
@login_required()
def show_image(request, server_id, image_id):
    """
    Show an image
    """

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        image_flag = ''

        if exists_active_collection_for_user(request.user):

            image_flag = 'ALLOW'

        else:

            image_flag = 'DISALLOW'

        data.update({ 'image_flag': image_flag })

        server = get_object_or_404(Server, pk=server_id)

        if server.is_omero547() or server.is_omero56():

            server_data = server.get_imaging_server_image_json(request, image_id)

            data.update(server_data)

            return render(request, 'gallery/show_image.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))


#
# SHOW THE AVAILABLE IMAGES
#  FROM A WORDPRESS SERVER
#
@login_required()
def show_wordpress(request, server_id, page_id):
    """
    Show the Wordpress Server
    """

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if server.is_wordpress():

            server_data = server.get_wordpress_json(request, page_id)

            data.update(server_data)

            return render(request, 'gallery/show_wordpress.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))


#
# SHOW AN IMAGE
#  FROM A WORDPRESS SERVER
#
@login_required()
def show_wordpress_image(request, server_id, image_id):
    """
    Show an image
    """

    data = get_header_data(request.user)

    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        if server.is_wordpress():

            server_data = server.get_wordpress_image_json(request, image_id)

            data.update(server_data)

            return render(request, 'gallery/show_wordpress_image.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))



#
# ADD A NEW IMAGE FROM AN IMAGE SERVER TO THE ACTIVE COLLECTION
#
@login_required
def add_image(request, server_id, image_id, roi_id):

    data = get_header_data(request.user)

    if not exists_active_collection_for_user(request.user):

        return HttpResponseRedirect(reverse('home', args=()))


    if data["credential_flag"] == NO_CREDENTIALS:

        return HttpResponseRedirect(reverse('home', args=()))

    else:

        server = get_object_or_404(Server, pk=server_id)

        image_count = get_image_count_for_image(image_id)

        json_image = ''
        name = ''
        viewer_url = ''
        birdseye_url = ''

        if server.is_omero547() or server.is_omero56():

            wp_data = server.get_imaging_server_image_json(request, image_id)

            json_image = wp_data['image']
            name = json_image['name']
            viewer_url = json_image['viewer_url']
            birdseye_url = json_image['birdseye_url']

            data.update(wp_data)

        if server.is_wordpress():

            wp_data = server.get_wordpress_image_json(request, image_id)

            json_image = wp_data['image']
            name = json_image['name']
            viewer_url = json_image['viewer_url']
            birdseye_url = json_image['thumbnail_url']

            data.update(wp_data)

        if roi_id == 0:

            if exists_active_collection_for_user(request.user):

                image = Image.create(image_id, name, server, viewer_url, birdseye_url, 0, request.user)

                image.save()

                queryset = get_active_collection_for_user(request.user)

                for collection in queryset:

                    Collection.assign_image(image, collection)

            else:

                messages.error(request, "You have no Active Image Collection; Please create a Collection!")

        else:

            json_rois = data['rois']

            for rois in json_rois:

                for shape in rois['shapes']:

                    if shape['id'] == int(roi_id):

                        viewer_url = shape['viewer_url']
                        birdseye_url = shape['shape_url']

                        if exists_active_collection_for_user(request.user):

                            image = Image.create(image_id, name, server, viewer_url, birdseye_url, roi_id, request.user)

                            image.save()

                            queryset = get_active_collection_for_user(request.user)

                            for collection in queryset:

                                Collection.assign_image(image, collection)

                        else:

                            messages.error(request, "You have no Active Image Collection; Please create a Collection!")

        if server.is_omero547() or server.is_omero56():

            return HttpResponseRedirect(reverse('webgallery_show_image', args=(server_id, image_id)))

        else:

            if server.is_wordpress():

                return HttpResponseRedirect(reverse('webgallery_show_wordpress_image', args=(server_id, image_id)))
