#!/usr/bin/python3
###!
# \file         convert_url_omero_image_to_cpw.py
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
# try to convert an OMERO URL to a CPW Equivalent?
###
from __future__ import unicode_literals

from urllib.parse import urlparse

from matrices.routines.exists_server_for_url import exists_server_for_url
from matrices.routines.get_server_list_for_url import get_server_list_for_url
from matrices.routines.validate_an_omero_image_url import validate_an_omero_image_url
from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment


#
#   Try to convert an OMERO URL to a CPW Equivalent?
#
def convert_url_omero_image_to_cpw(request, a_url):

    environment = get_primary_cpw_environment()

    url_string_out = ""

    if validate_an_omero_image_url(a_url):

        u = urlparse(a_url)

        server_url = u.netloc
        query_url = u.query

        query_array = query_url.split("=")
        query_params = query_array[1].split("-")
        query_type = query_params[0].lower()
        query_id = query_params[1]

        first_server = None

        if exists_server_for_url(server_url):

            server_list = get_server_list_for_url(server_url)

            for server in server_list:

                if not server.is_wordpress():

                    if query_type == "image":

                        server_data = {}

                        if environment.is_web_gateway() or server.is_idr():

                            server_data = server.get_imaging_server_image_json(query_id)

                        else:

                            if environment.is_blitz_gateway():

                                server_data = server.get_imaging_server_image_json_blitz(str(query_id))

                        image = server_data["image"]

                        if image["name"] != "ERROR":

                            first_server = server
                            break

            if request.is_secure():

                protocol = 'https'

            else:

                protocol = 'http'

            host = request.get_host()

            if first_server is not None:

                if query_type == "image":

                    url_start = protocol + "://" + host
                    url_end = "/show_image/" + str(first_server.id) + "/" + query_id
                    url_string_out = url_start + url_end

    return url_string_out
