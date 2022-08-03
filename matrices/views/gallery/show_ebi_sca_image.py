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
#
# This file contains the show_ebi_sca_image view routine
#
###
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from matrices.models import Server
from matrices.models import Image
from matrices.models import Document

from matrices.routines import credential_exists
from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import get_an_ebi_sca_experiment_id_from_chart_id
from matrices.routines import get_an_ebi_sca_parameters_from_chart_id


#
# SHOW A CHART FROM AN EBI SCA SERVER
#
@login_required()
def show_ebi_sca_image(request, server_id, image_id):
    """
    Show a chart from an EBI SCA Server
    """

    data = get_header_data(request.user)

    if credential_exists(request.user):

        server = get_object_or_404(Server, pk=server_id)

        if server.is_ebi_sca():

            image_flag = False

            if exists_active_collection_for_user(request.user):

                image_flag = True

            experiment_id = get_an_ebi_sca_experiment_id_from_chart_id(image_id)

            metadata = server.get_ebi_server_experiment_metadata(experiment_id)

            chart = get_an_ebi_sca_parameters_from_chart_id(server.url_server, image_id)

            image_comment = ''

            document_key = '/' + image_id

            if Document.objects.filter(location=document_key).exists():

                document = Document.objects.get(location=document_key)

                image_comment = document.comment

            if Image.objects.filter(name=image_id).exists():

                image = Image.objects.get(name=image_id)

                image_comment = image.comment


            data.update({ 'image_comment': image_comment, 'image_flag': image_flag, 'add_from': "show_image", 'server': server, 'chart': chart, 'metadata': metadata, 'add_from': "show_ebi_sca_image" })

            return render(request, 'gallery/show_ebi_sca_image.html', data)

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
