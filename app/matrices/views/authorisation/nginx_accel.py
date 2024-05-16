#!/usr/bin/python3
# \file         nginx_accel.py
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
# The ProtectedMediaRelay ViewSet
###
from __future__ import unicode_literals

import subprocess

from django.http import HttpResponse
from django.http import HttpResponseForbidden

from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment
from matrices.routines.exists_image_in_public_bench import exists_image_in_public_bench


#
#   nginx_accel
#
def nginx_accel(request, image_id):

    environment = get_primary_cpw_environment()

    filepath = environment.document_root + '/' + image_id

    test_command = 'echo $(test -f ' + filepath + ') $?'

    process = subprocess.Popen(test_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)

    out_list = process.stdout.readlines()

    file_exists = True

    for output in out_list:

        number = int(output)

        if number != 0:

            file_exists = False

    #   do your permission things here, and set file_exists to True if applicable
    if file_exists:

        if request.user.is_authenticated is True:

            response = HttpResponse()

            url = '/' + environment.nginx_private_location + '/' + image_id

            response['Content-Type'] = ""
            response['X-Accel-Redirect'] = url

            return response

        else:

            fullwebroot = environment.get_full_web_root() + '/' + image_id

            public_bench_exists = exists_image_in_public_bench(fullwebroot)

            if public_bench_exists is True:

                response = HttpResponse()

                url = '/' + environment.nginx_private_location + '/' + image_id

                response['Content-Type'] = ""
                response['X-Accel-Redirect'] = url

                return response

            else:

                return HttpResponseForbidden()

    else:

        return HttpResponseForbidden()
