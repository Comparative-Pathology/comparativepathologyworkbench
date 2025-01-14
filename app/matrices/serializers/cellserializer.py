#!/usr/bin/python3
# 
# ##
# \file         cellserializer.py
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
# This Serializer provides Read functions for a Cell ONLY
# ##
#
from rest_framework import serializers

from matrices.models import Cell

from matrices.serializers import ImageSerializer


class CellSerializer(serializers.HyperlinkedModelSerializer):
    """A Serializer of Cells

    A Serializer of Cells in the Comparative Pathology Workbench REST Interface

    This Serializer provides Read functions for a Cell ONLY

    Parameters:
        url(Read Only): The (internal) URL of the Cell.

        title: The Title of the Cell.
        description: The Description of the Cell.
        column_index: The X Coordinate of the Cell.
        row_index: The Y Coordinate of the Cell.
        cell_id: The identifier of the Cell.
        image: An Image Object or None, associated with the Cell

    """

    title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    description = serializers.CharField(max_length=4095, required=False, allow_blank=True)
    column_index = serializers.IntegerField(source='xcoordinate')
    row_index = serializers.IntegerField(source='ycoordinate')
    cell_id = serializers.IntegerField(source='id')

    image = ImageSerializer(many=False, allow_null=True)

    class Meta:
        model = Cell
        fields = ('url', 'cell_id', 'title', 'description', 'column_index', 'row_index', 'image')
        read_only_fields = ('url', )
