#!/usr/bin/python3
###!
# \file         views_authorisation.py
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
# This file contains the collectivization view routine
#
###
from __future__ import unicode_literals

from django.http import HttpResponseRedirect

from django.shortcuts import render

from matrices.models import Image
from matrices.models import Server

from matrices.routines import get_header_data
from matrices.routines import get_images_for_user

#
# SETUP DEFAULT COLLECTIONS VIEW
#
def renaming(request):

    data = get_header_data(request.user)

    if request.user.is_superuser:

        image_list = Image.objects.all()

        out_message_list = list()

        imageTotal = 0
        imageChanged = 0
        imageNotChanged = 0

        out_message = ""

        for image in image_list:

            imageTotal = imageTotal + 1

            if image.server.is_omero547():

                name_array = image.name.split("/")

                if len(name_array) >= 4:

                    imageNotChanged = imageNotChanged + 1

                else:

                    wp_data = image.server.get_imaging_server_image_json(image.identifier)

                    group = wp_data['group']
                    group_name = group['name']

                    project_name = ""
                    dataset_name = ""
                    image_name = ""
                    full_image_name = ""

                    projects = wp_data['projects']

                    if len(projects) > 0:

                        project = projects[0]
                        project_name = project['name']

                    datasets = wp_data['datasets']

                    if len(datasets) > 0:

                        dataset = datasets[0]
                        dataset_name = dataset['name']

                    json_image = wp_data['image']
                    image_name = json_image['name']

                    if image_name == 'ERROR':

                        imageNotChanged = imageNotChanged + 1

                    else:

                        if len(projects) > 0 and len(datasets) > 0:

                            full_image_name = group_name + "/" + project_name + "/" + dataset_name + "/" + image_name

                        else:

                            full_image_name = image_name

                        if image.name == full_image_name:

                            imageNotChanged = imageNotChanged + 1

                        else:

                            imageChanged = imageChanged + 1

                            image.set_name(full_image_name)
                            image.save()

            else:

                imageNotChanged = imageNotChanged + 1

        out_message = "Total Number of Images {}".format( imageTotal )
        out_message_list.append(out_message)

        out_message = "Total Number of Images Changed {}".format( imageChanged )
        out_message_list.append(out_message)

        out_message = "Total Number of Images Not Changed {}".format( imageNotChanged )
        out_message_list.append(out_message)

        data.update({ 'out_message_list': out_message_list })

        return render(request, 'authorisation/renaming.html', data)

    else:

        return HttpResponseRedirect(reverse('home', args=()))
