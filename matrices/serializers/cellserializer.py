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

