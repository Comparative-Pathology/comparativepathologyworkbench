#!/usr/bin/python3
#
# ##
# \file         delete_bench_task.py
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
# The delete_bench_task Task.
# ##
#
from __future__ import absolute_import

import subprocess

from celery import shared_task

from django.contrib.auth.models import User

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Credential

from matrices.routines import exists_collections_for_image
from matrices.routines import get_cells_for_image
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment
from matrices.routines.simulate_network_latency import simulate_network_latency


#
#   DELETE a Bench
#
@shared_task
def delete_bench_task(matrix_id, user_id):

    simulate_network_latency()

    environment = get_primary_cpw_environment()

    user = User.objects.get(id=user_id)

    credential = Credential.objects.get_or_none(username=user.username)

    matrix = Matrix.objects.get(id=matrix_id)

    oldCells = Cell.objects.filter(matrix=matrix_id)

    out_message = ""

    if matrix.has_blogpost():

        if credential.has_apppwd() and environment.is_wordpress_active():

            response = environment.delete_a_post_from_wordpress(credential, matrix.blogpost)

    for oldCell in oldCells:

        if oldCell.has_blogpost():

            if credential.has_apppwd() and environment.is_wordpress_active():

                response = environment.delete_a_post_from_wordpress(credential, oldCell.blogpost)

        if oldCell.has_image():

            if exists_collections_for_image(oldCell.image):

                cell_list = get_cells_for_image(oldCell.image)

                other_bench_Flag = False

                for otherCell in cell_list:

                    if otherCell.matrix.id != matrix_id:

                        other_bench_Flag = True

                if other_bench_Flag is True:

                    if user.profile.is_hide_collection_image():

                        oldCell.image.set_hidden(True)
                        oldCell.image.save()

                    else:

                        oldCell.image.set_hidden(False)
                        oldCell.image.save()

                else:

                    oldCell.image.set_hidden(False)
                    oldCell.image.save()

            else:

                cell_list = get_cells_for_image(oldCell.image)

                delete_flag = True

                for otherCell in cell_list:

                    if otherCell.matrix.id != matrix_id:

                        delete_flag = False

                image = oldCell.image

                if delete_flag is True:

                    oldCell.image = None

                    oldCell.save()

                    if image.server.is_ebi_sca() or image.server.is_cpw():

                        image_path = environment.document_root + '/' + image.name

                        rm_command = 'rm ' + str(image_path)
                        rm_escaped = rm_command.replace("(", "\(").replace(")", "\)")

                        process = subprocess.Popen(rm_escaped,
                                                   shell=True,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   universal_newlines=True)

                    if image.server.is_omero547() and not image.server.is_idr():

                        image_path = environment.document_root + '/' + image.get_file_name_from_birdseye_url()

                        rm_command = 'rm ' + str(image_path)
                        rm_escaped = rm_command.replace("(", "\(").replace(")", "\)")

                        process = subprocess.Popen(rm_escaped,
                                                   shell=True,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   universal_newlines=True)

                    image.delete()

    out_message = 'Bench ' + matrix.get_formatted_id() + ' DELETED!'

    matrix.delete()

    return out_message
