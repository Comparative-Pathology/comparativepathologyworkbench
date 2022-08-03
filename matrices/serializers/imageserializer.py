#!/usr/bin/python3
###!
# \file         imageserializer.py
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
# This Serializer provides Create, Read, Update and Delete functions for an Image
###
from django.contrib.auth.models import User

from rest_framework import serializers

from django.db import models

from matrices.models import Image
from matrices.models import Server

from matrices.routines import exists_server_for_uid_url
from matrices.routines import get_servers_for_uid_url


"""
	This Serializer provides Create, Read, Update and Delete functions for an Image
"""
class ImageSerializer(serializers.HyperlinkedModelSerializer):

	roi = serializers.IntegerField(default=0)
	owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
	server = serializers.CharField()
	image_id = serializers.IntegerField(default=0)

	class Meta:
		model = Image
		fields = ('url', 'id', 'owner', 'roi', 'server', 'image_id')
		read_only_fields = ('id', 'url' )


	"""
		Image Serializer, Create Method
	"""
	def create(self, validated_data):

		request_user = None

		request = self.context.get("request")

		if request and hasattr(request, "user"):

			request_user = request.user

		image_server = validated_data.get('server')
		image_owner = validated_data.get('owner')
		image_id = validated_data.get('image_id')
		image_roi_id = validated_data.get('roi')

		if request_user != image_owner:

			if not request_user.is_superuser:

				message = 'CPW_REST:0060 ERROR! Attempting to Add a new Image for a different Owner: ' + str(image_owner) + '!'
				raise serializers.ValidationError(message)

		server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id)

		image_identifier = int(image_id)

		image_name = ''
		image_viewer_url = ''
		image_birdseye_url = ''
		image_roi = 0
		image_comment = ''

		if server.is_wordpress():

			data = server.check_wordpress_image(image_owner, image_id)

			json_image = data['image']

			image_name = json_image['name']
			image_viewer_url = json_image['viewer_url']
			image_birdseye_url = json_image['birdseye_url']

		else:

			data = server.check_imaging_server_image(image_owner, image_id)

			json_image = data['image']

			image_name = json_image['name']
			image_viewer_url = json_image['viewer_url']
			image_birdseye_url = json_image['birdseye_url']

			if image_roi_id != 0:

				data = server.check_imaging_server_image_roi(image_owner, image_id, image_roi_id)

				json_roi = data['roi']

				image_roi = int(json_roi['id'])

		image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_roi, image_owner, image_comment)

		image.save()

		return image


	"""
	Image Serializer, Update Method
	"""
	def update(self, instance, validated_data):

		image_server = validated_data.get('server')
		image_owner = validated_data.get('owner', instance.owner)
		image_id = validated_data.get('image_id', instance.image_id)
		image_roi_id = validated_data.get('roi', instance.roi)
		image_comment = validated_data.get('roi', instance.comment)

		server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id)

		image_identifier = int(image_id)
		image_name = ''
		image_viewer_url = ''
		image_birdseye_url = ''
		image_roi = 0
		image_comment = ''

		if server.is_wordpress():

			data = server.check_wordpress_image(image_owner.id, image_id)

			json_image = data['image']

			image_name = json_image['name']
			image_viewer_url = json_image['viewer_url']
			image_birdseye_url = json_image['birdseye_url']

		else:

			data = server.check_imaging_server_image(image_owner.id, image_id)

			json_image = data['image']

			image_name = json_image['name']
			image_viewer_url = json_image['viewer_url']
			image_birdseye_url = json_image['birdseye_url']

			if image_roi_id != 0:

				data = server.check_imaging_server_image_roi(image_owner, image_id, image_roi_id)

				json_roi = data['roi']

				image_roi = int(json_roi['id'])

		instance.server = server
		instance.owner = image_owner
		instance.image_id = image_id
		instance.identifier = image_id
		instance.name = image_name
		instance.viewer_url = image_viewer_url
		instance.birdseye_url = image_birdseye_url
		instance.roi = image_roi
		instance.comment = image_comment

		instance.save()

		return instance


	"""
		Image Serializer, For an Image, Validate the supplied Server, Owner, Image Id and ROI ID Fields
	"""
	def validate_image_json(self, server_str, user, image_id, roi_id):

		server_list = server_str.split("@")

		server_uid = str(server_list[0])
		server_url = str(server_list[1])

		if exists_server_for_uid_url(server_uid, server_url):

			server = get_servers_for_uid_url(server_uid, server_url)

			if server.is_wordpress():

				if not self.validate_wordpress_image_id(server, user, image_id):

					message = 'CPW_REST:0320 ERROR! Image NOT Present on : ' + server_str + '!'
					raise serializers.ValidationError(message)
			else:

				if server.is_omero547():

					if self.validate_imaging_image_id(server, user, image_id):

						if roi_id != 0:

							if not self.validate_roi_id(server, user, image_id, roi_id):

								message = 'CPW_REST:0240 ERROR! ROI ID ' + str(roi_id) + ', for Image ID ' + str(image_id) + ", NOT Present on : " + server_str + '!'
								raise serializers.ValidationError(message)
					else:

						message = 'CPW_REST:0200 ERROR! Image ID ' + str(image_id) + ', NOT Present on : ' + server_str + '!'
						raise serializers.ValidationError(message)
				else:

					message = 'CPW_REST:0340 ERROR! Server Type Unknown : ' + server_str + '!'
					raise serializers.ValidationError(message)

			return server

		else:

			message = 'CPW_REST:0260 ERROR! Server Unknown : ' + server_str + '!'
			raise serializers.ValidationError(message)

			return None


	"""
		Image Serializer, For a Wordpress Image, Check the supplied Image Exists
	"""
	def validate_wordpress_image_id(self, server, user, image_id):

		data = server.check_wordpress_image(user, image_id)

		json_image = data['image']
		image_name = json_image['name']

		if image_name == "":
			return False
		else:
			return True


	"""
		Image Serializer, For an OMERO Image, Check the supplied Image Exists
	"""
	def validate_imaging_image_id(self, server, user, image_id):

		data = server.check_imaging_server_image(user, image_id)

		json_image = data['image']
		image_name = json_image['name']

		if image_name == "":
			return False
		else:
			return True


	"""
		Image Serializer, For an OMERO Image ROI, Check the supplied ROI Exists
	"""
	def validate_roi_id(self, server, user, image_id, roi_id):

		data = server.check_imaging_server_image_roi(user, image_id, roi_id)

		json_roi = data['roi']
		roi_id = json_roi['id']

		if roi_id == "":
			return False
		else:
			return True
