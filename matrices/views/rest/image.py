#!/usr/bin/python3
###!
# \file         image.py
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
# The Image View Set automatically provides `list`, `create`, `retrieve`,
# `update` and `destroy` actions.
###
from __future__ import unicode_literals

from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from matrices.models import Image

from matrices.permissions import ImageIsReadOnlyOrIsAdminOrIsOwner

from matrices.serializers import ImageSerializer

#
# BENCH CELL IMAGE REST INTERFACE ROUTINES
#
class ImageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`, `update` and `destroy` actions.
    """
    queryset = Image.objects.all()

    serializer_class = ImageSerializer

    permission_classes = ( permissions.IsAuthenticated,
                           ImageIsReadOnlyOrIsAdminOrIsOwner )


    def partial_update(self, request, *args, **kwargs):

        return Response(data='Image PARTIAL UPDATE Not Available')

    def list(self, request, *args, **kwargs):

        return Response(data='Image LIST Not Available')
