#!/usr/bin/python3
###!
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
# This Serializer provides Read functions for a CELL
###
from django.contrib.auth.models import User

from rest_framework import serializers

from django.db import models
from django.db.models import Q

from matrices.models import Cell

from matrices.serializers import ImageSerializer


"""
	This Serializer provides Read functions for a CELL
"""
class CellSerializer(serializers.HyperlinkedModelSerializer):

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
