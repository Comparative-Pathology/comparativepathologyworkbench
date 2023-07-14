#!/usr/bin/python3
###!
# \file         edit_image.py
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
# This file contains the edit_image view routine
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

from matrices.routines import credential_exists
from matrices.routines import exists_active_collection_for_user
from matrices.routines import get_header_data
from matrices.routines import get_credential_for_user
from matrices.routines import get_an_ebi_sca_experiment_id_from_chart_id
from matrices.routines import get_an_ebi_sca_parameters_from_chart_id


@login_required()
def edit_image(request, image_id):
    """
    Edit an image
    """

    data = get_header_data(request.user)

    local_image = get_object_or_404(Image, pk=image_id)

    credential = get_credential_for_user(request.user)

    common_tags = Image.tags.most_common()
    used_tags = local_image.tags.all()
    all_unused_tags = set(common_tags).difference(set(used_tags))
    unused_tags = list(all_unused_tags)[:10]

    data.update({ 'unused_tags': unused_tags })

    template = ''

    if credential_exists(request.user):

        server = get_object_or_404(Server, pk=local_image.server_id)

        data.update({ 'local_image': local_image })

        if server.is_wordpress():

            server_data = server.get_wordpress_image_json(credential, image_id)

            data.update(server_data)
            data.update({ 'image': local_image })

            template = 'gallery/edit_wordpress_image.html'

        if server.is_omero547():

            server_data = server.get_imaging_server_image_json(local_image.identifier)

            data.update(server_data)

            template = 'gallery/edit_image.html'

        if server.is_cpw():

            chart = ({
                'chart_id': local_image.name,
                'viewer_url': local_image.viewer_url,
                'birdseye_url': local_image.birdseye_url,
            })

            data.update({ 'image_url': local_image.viewer_url, 'image_comment': local_image.comment, 'server': server, 'chart': chart })

            template = 'gallery/edit_cpw_image.html'

        if server.is_ebi_sca():

            experiment_id = get_an_ebi_sca_experiment_id_from_chart_id(local_image.name)

            metadata = server.get_ebi_server_experiment_metadata(experiment_id)

            chart = get_an_ebi_sca_parameters_from_chart_id(server.url_server, local_image.name)

            data.update({ 'image_comment': local_image.comment, 'server': server, 'chart': chart, 'metadata': metadata })

            template = 'gallery/edit_ebi_sca_image.html'

        return render(request, template, data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
