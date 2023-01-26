#!/usr/bin/python3
###!
# \file         exists_image_on_webserver.py
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
# Is there an Image for a particular Server?
###
from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps
from django.conf import settings

from decouple import config


"""
    Is there an Image for a particular Image on the Webserver?
"""
def exists_image_on_webserver(an_image_name):

    Image = apps.get_model('matrices', 'Image')

    a_viewer_url = settings.HIGHCHARTS_OUTPUT_WEB + an_image_name

    return Image.objects.filter(viewer_url=a_viewer_url).exists()