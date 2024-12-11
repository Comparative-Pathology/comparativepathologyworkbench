#!/usr/bin/python3
#
# ##
# \file         delete_bench.py
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
# This file contains the AJAX delete_bench view routine
# ##
#
from __future__ import unicode_literals

import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Credential

from matrices.routines import exists_collections_for_image
from matrices.routines import get_cells_for_image
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment

from background.tasks import delete_bench_task

WORDPRESS_SUCCESS = 'Success!'


#
#   DELETE A BENCH
#
@login_required()
def delete_bench(request, bench_id):

    if not request.user.is_authenticated:

        raise PermissionDenied

    credential = Credential.objects.get_or_none(username=request.user.username)

    if not credential:

        raise PermissionDenied

    if credential.has_no_apppwd():

        raise PermissionDenied

    matrix = Matrix.objects.get_or_none(id=bench_id)

    if not matrix:

        raise PermissionDenied

    if matrix.is_locked():

        raise PermissionDenied

    environment = get_primary_cpw_environment()

    if environment.is_background_processing():

        matrix.set_locked()
        matrix.save()

        result = delete_bench_task.delay_on_commit(matrix.id, request.user.id)

        messages.error(request, 'Bench ' + matrix.get_formatted_id() + ' LOCKED pending Delete!')

    else:

        oldCells = Cell.objects.filter(matrix=bench_id)

        if matrix.has_blogpost():

            if credential.has_apppwd() and environment.is_wordpress_active():

                response = environment.delete_a_post_from_wordpress(credential, matrix.blogpost)

                if response != WORDPRESS_SUCCESS:

                    messages.error(request, "CPW_WEB:0560 Delete Bench - WordPress Error, Contact System " +
                                   "Administrator!")

        for oldCell in oldCells:

            if oldCell.has_blogpost():

                if credential.has_apppwd() and environment.is_wordpress_active():

                    response = environment.delete_a_post_from_wordpress(credential, oldCell.blogpost)

                    if response != WORDPRESS_SUCCESS:

                        messages.error(request, "CPW_WEB:0550 Delete Bench - WordPress Error, Contact System " +
                                       "Administrator!")

            if oldCell.has_image():

                if exists_collections_for_image(oldCell.image):

                    cell_list = get_cells_for_image(oldCell.image)

                    other_bench_Flag = False

                    for otherCell in cell_list:

                        if otherCell.matrix.id != bench_id:

                            other_bench_Flag = True

                    if other_bench_Flag is True:

                        if request.user.profile.is_hide_collection_image():

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

                        if otherCell.matrix.id != bench_id:

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

        messages.success(request, 'Bench ' + matrix.get_formatted_id() + ' DELETED!')

        matrix.delete()

    return HttpResponseRedirect(reverse('list_benches', args=()))
