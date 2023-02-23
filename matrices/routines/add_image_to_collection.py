#!/usr/bin/python3
###!
# \file         add_image_to_collection.py
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
# This file contains the add_image_to_collection routine
#
###
from __future__ import unicode_literals

import os
import time

from datetime import datetime

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from decouple import config

from matrices.routines.get_active_collection_for_user import get_active_collection_for_user
from matrices.routines.get_image_count_for_image import get_image_count_for_image
from matrices.routines.exists_image_for_id_server_owner_roi import exists_image_for_id_server_owner_roi
from matrices.routines.get_images_for_id_server_owner_roi import get_images_for_id_server_owner_roi
from matrices.routines.get_an_ebi_sca_experiment_id_from_chart_id import get_an_ebi_sca_experiment_id_from_chart_id
from matrices.routines.get_an_ebi_sca_parameters_from_chart_id import get_an_ebi_sca_parameters_from_chart_id

#
# ADD A NEW IMAGE FROM AN IMAGE SERVER TO THE ACTIVE COLLECTION
#
def add_image_to_collection(credential, server, image_id, roi_id):

    Image = apps.get_model('matrices', 'Image')
    Collection = apps.get_model('matrices', 'Collection')
    Document = apps.get_model('matrices', 'Document')

    user = User.objects.get(username=credential.username)

    image_out = None

    comment = ''

    json_image = ''
    image_name = ''
    image_viewer_url = ''
    image_birdseye_url = ''
    image_comment = ''
    image_hidden = False
    full_image_name = image_id
    image_key = ''
    document_key = ''


    if server.is_cpw():

        now = datetime.now()
        date_time = now.strftime('%Y%m%d-%H:%M:%S.%f')[:-3]

        new_datetime = date_time.replace('-', '').replace(':', '').replace('.', '')

        size = len(new_datetime)

        image_key = new_datetime[8:size + 9]

        document_key = '/' + image_id

        image_birdseye_url = 'http://' + server.url_server + document_key

        image_id = image_key

        if Document.objects.filter(location=document_key).filter(owner=user).exists():

            documents_list = Document.objects.filter(location=document_key).filter(owner=user)

            for document in documents_list:

                image_comment = document.comment
                image_viewer_url = document.source_url


    if server.is_ebi_sca():

        experiment_id = get_an_ebi_sca_experiment_id_from_chart_id(image_id)

        metadata = server.get_ebi_server_experiment_metadata(experiment_id)

        chart = get_an_ebi_sca_parameters_from_chart_id(server.url_server, image_id)

        image_id = int(chart['chart_key'])
        full_image_name = chart['chart_id']
        image_viewer_url = chart['viewer_url']
        image_birdseye_url = chart['birdseye_url']

        document_key = '/' + full_image_name


    if server.is_omero547():

        wp_data = server.get_imaging_server_image_json(image_id)

        group = wp_data['group']
        group_name = group['name']

        projects = wp_data['projects']
        project = projects[0]
        project_name = project['name']

        datasets = wp_data['datasets']
        dataset = datasets[0]
        dataset_name = dataset['name']

        json_image = wp_data['image']
        image_name = json_image['name']

        full_image_name = group_name + "/" + project_name + "/" + dataset_name + "/" + image_name

        image_viewer_url = json_image['viewer_url']
        image_birdseye_url = json_image['birdseye_url']


    if server.is_wordpress():

        wp_data = server.get_wordpress_image_json(credential, image_id)

        json_image = wp_data['image']
        full_image_name = json_image['name']
        image_viewer_url = json_image['viewer_url']
        image_birdseye_url = json_image['thumbnail_url']


    if roi_id == 0:

        if document_key != '':

            if Document.objects.filter(location=document_key).filter(owner=user).exists():

                documents_list = Document.objects.filter(location=document_key).filter(owner=user)

                for document in documents_list:

                    document.delete()

        if exists_image_for_id_server_owner_roi(image_id, server, user, 0):

            existing_image_list = get_images_for_id_server_owner_roi(image_id, server, user, 0)

            image_out = existing_image_list[0]

        else:

            image_out = Image.create(image_id, full_image_name, server, image_viewer_url, image_birdseye_url, roi_id, user, image_comment, image_hidden)

            image_out.save()

        collection = get_active_collection_for_user(user)

        Collection.assign_image(image_out, collection)


    else:

        json_rois = wp_data['rois']

        for rois in json_rois:

            for shape in rois['shapes']:

                if shape['id'] == int(roi_id):

                    image_viewer_url = shape['viewer_url']
                    image_birdseye_url = shape['shape_url']

                    if exists_image_for_id_server_owner_roi(image_id, server, user, roi_id):

                        existing_image_list = get_images_for_id_server_owner_roi(image_id, server, user, roi_id)

                        image_out = existing_image_list[0]

                    else:

                        image_out = Image.create(image_id, full_image_name, server, image_viewer_url, image_birdseye_url, roi_id, user, comment, image_hidden)

                        image_out.save()

                    collection = get_active_collection_for_user(user)

                    Collection.assign_image(image_out, collection)

    return image_out
