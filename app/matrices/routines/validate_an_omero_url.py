#!/usr/bin/python3
###!
# \file         validate_an_omero_url.py
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
# Do we have a valid OMERO URL?
###
from __future__ import unicode_literals

import base64, hashlib

from urllib.parse import urlparse


"""
    Do we have a Valid OMERO URL?
"""
def validate_an_omero_url(a_url):

    result = urlparse(a_url)

    if all([result.scheme, result.netloc, result.path, result.query]):

        query_url = result.query

        query_array = query_url.split("=")

        if len(query_array) != 2:

            return False

        query_params = query_array[1].split("-")

        if len(query_params) != 2:

            return False

        query_prefix = query_array[0].lower()

        if query_prefix != "show":
            return False


        query_type = query_params[0].lower()

        if not (query_type == "image" or query_type == "dataset" or query_type == "project"):

            return False


        query_id = query_params[1]

        if not query_id.isnumeric():

            return False


        return True

    else:

        return False
