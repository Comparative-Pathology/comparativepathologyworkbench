#!/usr/bin/python3
#
# ##
# \file         show_cpw_image.py
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
# This file contains the show_ebi_sca_image view routine
# ##
#
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from matrices.models import Server
from matrices.models import Image
from matrices.models import Document
from matrices.models import Credential

from matrices.routines import get_header_data


#
#   SHOW A CHART FROM AN EBI SCA SERVER
#
@login_required()
def show_cpw_image(request, server_id, image_id):

    if request.user.username == 'guest':

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if credential:

        server = Server.objects.get_or_none(id=server_id)

        if server:

            if server.is_cpw():

                image_flag = False

                if request.user.profile.has_active_collection():

                    image_flag = True

                viewer_url = 'http://' + server.url_server + '/' + image_id
                birdseye_url = 'http://' + server.url_server + '/' + image_id

                image_comment = ''
                image_url = ''

                document_key = '/' + image_id

                if Document.objects.filter(location=document_key).filter(owner=request.user).exists():

                    documents_list = Document.objects.filter(owner=request.user).filter(location=document_key)

                    for document in documents_list:

                        image_comment = document.comment
                        image_url = document.source_url

                if Image.objects.filter(name=image_id).exists():

                    image = Image.objects.get(name=image_id)

                    image_comment = image.comment
                    image_url = image.viewer_url

                chart = ({
                    'chart_id': image_id,
                    'viewer_url': viewer_url,
                    'birdseye_url': birdseye_url,
                })

                data = get_header_data(request.user)

                data.update({'image_url': image_url,
                             'image_comment': image_comment,
                             'image_flag': image_flag,
                             'server': server,
                             'chart': chart,
                             'add_from': "show_cpw_image"})

                return render(request, 'gallery/show_cpw_image.html', data)

            else:

                return HttpResponseRedirect(reverse('home', args=()))

        else:

            return HttpResponseRedirect(reverse('home', args=()))

    else:

        return HttpResponseRedirect(reverse('home', args=()))
