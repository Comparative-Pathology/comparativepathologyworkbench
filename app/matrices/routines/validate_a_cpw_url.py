#!/usr/bin/python3
#
# ##
# \file         validate_a_cpw_url.py
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
# Do we have a valid EBI Single Cell Atlas URL?
# ##
#
from __future__ import unicode_literals

from urllib.parse import urlparse


#
#   Do we have a Valid CPW URL?
#
def validate_a_cpw_url(a_url):

    protocol_list = ["http", "https"]

    result = urlparse(a_url)

    if all([result.scheme, result.netloc, result.path]):

        if result.scheme.lower() in protocol_list:

            if result.path.lower() == '/':

                return False

            else:

                return True

        else:

            return False

    else:

        return False
