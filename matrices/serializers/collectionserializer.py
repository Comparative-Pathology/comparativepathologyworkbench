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
# This Serializer provides Read functions for a Collection
###
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404

from django.db import models
from django.db.models import Q

from matrices.models import Collection
from matrices.models import Image

from matrices.serializers import ImageSerializer

from matrices.routines import exists_image_for_id_server_owner_roi
from matrices.routines import get_images_for_id_server_owner_roi
from matrices.routines import exists_server_for_uid_url
from matrices.routines import get_servers_for_uid_url
from matrices.routines import exists_active_collection_for_user
from matrices.routines import set_inactive_collection_for_user
from matrices.routines import get_collections_for_image
from matrices.routines import get_images_for_collection

CONST_255 = 255
CONST_4095 = 4095


"""
	This Serializer provides Create, Read, Update and Delete functions for a COLLECTION
"""
class CollectionSerializer(serializers.HyperlinkedModelSerializer):

	title = serializers.CharField(max_length=255, required=False, allow_blank=True)
	description = serializers.CharField(max_length=4095, required=False, allow_blank=True)
	active = serializers.BooleanField(required=True)
	owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

	#images = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True)
	images = ImageSerializer(many=True, required=False)

	class Meta:
		model = Collection
		fields = ('url', 'id', 'title', 'description', 'active', 'owner', 'images')
		read_only_fields = ('url', )


	"""
		Collection Serializer, Create Method
	"""
	def create(self, validated_data):

		request_user = None

		request = self.context.get("request")

		if request and hasattr(request, "user"):

			request_user = request.user

		else:

			user_id = Token.objects.get(key=request.auth.key).user_id
			request_user = User.objects.get(id=user_id)


		if validated_data.get('title', None) == None and validated_data.get('description', None) == None:

			message = 'CPW0300: ERROR! NO data supplied for Collection Creation!'
			raise serializers.ValidationError(message)


		collection_title = ""
		collection_description = ""
		collection_active = False

		if validated_data.get('title', None) == None:

			collection_title = ""

		else:

			collection_title = validated_data.get('title')


		if validated_data.get('description', None) == None:

			collection_description = ""

		else:

			collection_description = validated_data.get('description')


		if validated_data.get('active') == True:

			collection_active = True

		else:

			collection_active = False


		collection_owner = validated_data.get('owner')

		if request_user != collection_owner:

			if not request_user.is_superuser:

				message = 'CPW0310: ERROR! Attempting to Add a new Collection for a different Owner: ' + str(collection_owner) + '!'
				raise serializers.ValidationError(message)


		self.validate_collection_json_fields(collection_title, collection_description)

		collection = None

		image_list = list()

		if validated_data.get('images', None) == None:

			collection = Collection.create(collection_title, collection_description, collection_active, collection_owner)

		else:

			images_data = validated_data.pop('images')

			create_flag = True

			self.validate_collection_images(images_data, request_user, create_flag)

			collection = Collection.create(collection_title, collection_description, collection_active, collection_owner)

			for image_data in images_data:

				image = image_data.get('image')

				image_server = image_data.get('server')
				image_owner = image_data.get('owner')
				image_id = image_data.get('image_id')
				image_roi_id = image_data.get('roi')

				server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id)

				image_identifier = int(image_id)

				image_name = ''
				image_viewer_url = ''
				image_birdseye_url = ''
				image_roi = image_roi_id

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

						data = server.get_imaging_server_image_roi_json(image_id, image_roi_id)

						json_roi = data['roi']
						shape = json_roi['shape']

						image_viewer_url = shape['viewer_url']
						image_birdseye_url = shape['shape_url']


				if exists_image_for_id_server_owner_roi(image_id, server, image_owner, image_roi):

					existing_image_list = get_images_for_id_server_owner_roi(image_id, server, image_owner, image_roi)

					image_in = existing_image_list[0]

					image_list.append(image_in)

				else:

					image_in = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_roi, image_owner)

					image_in.save()

					image_list.append(image_in)


		if collection.is_active():

			if exists_active_collection_for_user(request.user):

				set_inactive_collection_for_user(request.user)


		collection.save()


		for image_out in image_list:

			Collection.assign_image(image_out, collection)


		return collection


	"""
		Collection Serializer, Update Method
	"""
	def update(self, instance, validated_data):

		request_user = None

		request = self.context.get("request")

		if request and hasattr(request, "user"):

			request_user = request.user

		else:

			user_id = Token.objects.get(key=request.auth.key).user_id
			request_user = User.objects.get(id=user_id)


		collection_title = validated_data.get('title', instance.title)
		collection_description = validated_data.get('description', instance.description)
		collection_owner = validated_data.get('owner', instance.owner)

		if request_user != collection_owner:

			if not request_user.is_superuser:

				message = 'CPW0320: ERROR! Attempting to Update an existing Collection for a different Owner: ' + str(collection_owner) + '!'
				raise serializers.ValidationError(message)


		self.validate_collection_json_fields(collection_title, collection_description)

		images_data = []

		if validated_data.get('images', None) != None:

			images_data = validated_data.pop('images')

		create_flag = False

		self.validate_collection_images(images_data, request_user, create_flag)

		self.delete_missing_images(instance, request_user, images_data)

		self.add_new_images(instance, request_user, images_data)

		instance.title = collection_title
		instance.description = collection_description

		instance.save()

		return instance



	"""
		Collection Serializer, For a Collection, Validate the supplied Title and Description fields
	"""
	def validate_collection_json_fields(self, title, description):

		len_title = len(title)
		len_description = len(description)

		"""
			Title and Description field overflows are trapped by the Django REST framework,
		 	so these next 2 checks are redundant
		"""
		if len_title > CONST_255:

			message = 'CPW0340: ERROR! Collection Title Length (' + str(len_title) + ') is greater than 255!'
			raise serializers.ValidationError(message)

		if len_description > CONST_4095:

			message = 'CPW0350: ERROR! Collection Description Length (' + str(len_title) + ') is greater than 4095!'
			raise serializers.ValidationError(message)


	"""
		Collection Serializer, For a Collection, Delete any Missing Images
	"""
	def delete_missing_images(self, instance, request_user, images_data):

		delete_image_list = list()

		image_id_input_list = list()
		image_id_exist_list = list()

		images = (instance.images).all()
		images = list(images)

		for image_data in images_data:

			image_id = image_data.get('image_id', 0)

			image_id_input_list.append(image_id)


		for collection_image in images:

			collection_image_id = collection_image.identifier

			image_id_exist_list.append(collection_image_id)


		set_difference = set(image_id_exist_list) - set(image_id_input_list)
		delete_image_list = list(set_difference)

		for delete_image_id in delete_image_list:

			images = get_images_for_collection(instance)

			for image in images:

				if delete_image_id == image.identifier:

					collection_list = get_collections_for_image(image)

					delete_flag = True

					for collection_other in collection_list:

						if instance != collection_other:

							delete_flag = False

						if delete_flag == True:

							image.delete()

						else:

							Collection.unassign_image(image, instance)


	"""
		Collection Serializer, For a Collection, Add New Images
	"""
	def add_new_images(self, instance, request_user, images_data):

		add_image_list = list()

		image_id_input_list = list()
		image_id_exist_list = list()

		images = (instance.images).all()
		images = list(images)


		for image_data in images_data:

			image_id = image_data.get('image_id', 0)

			image_id_input_list.append(image_id)


		for collection_image in images:

			collection_image_id = collection_image.identifier

			image_id_exist_list.append(collection_image_id)


		set_difference = set(image_id_input_list) - set(image_id_exist_list)
		add_image_list = list(set_difference)

		"""
			Add NEW IMAGES
		"""
		for add_image_id in add_image_list:

			for image_data in images_data:

				image_id = image_data.get('image_id', 0)

				new_image = None

				if image_id == add_image_id:

					server = image_data.get('server')
					owner = image_data.get('owner')
					image_id = image_data.get('image_id')
					roi_id = image_data.get('roi')

					server = self.validate_image_json(server, owner, image_id, roi_id)

					image_identifier = int(image_id)

					image_name = ''
					image_viewer_url = ''
					image_birdseye_url = ''
					image_roi = 0

					if server.is_wordpress():

						data = server.check_wordpress_image(owner, image_id)

						json_image = data['image']

						image_name = json_image['name']
						image_viewer_url = json_image['viewer_url']
						image_birdseye_url = json_image['birdseye_url']

					else:

						data = server.check_imaging_server_image(owner, image_id)

						json_image = data['image']

						image_name = json_image['name']
						image_viewer_url = json_image['viewer_url']
						image_birdseye_url = json_image['birdseye_url']

						if roi_id != 0:

							data = server.check_imaging_server_image_roi(owner, image_id, roi_id)

							json_roi = data['roi']

							image_roi = int(json_roi['id'])


					if exists_image_for_id_server_owner_roi(image_id, server, owner, image_roi):

						existing_image_list = get_images_for_id_server_owner_roi(image_id, server, owner, image_roi)

						existing_image = existing_image_list[0]

						new_image = existing_image

						Collection.assign_image(new_image, instance)

					else:

						new_image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_roi, owner)

						new_image.save()

						Collection.assign_image(new_image, instance)


	"""
		Collection Serializer, For a Collection, Validate the supplied Images
	"""
	def validate_collection_images(self, images_data, request_user, mode_flag):

		for image_data in images_data:

			image = image_data.get('image')

			if image is not None:

				server = image.get('server')
				image_owner = image.get('owner')
				image_id = image.get('image_id')
				roi_id = image.get('roi')

				if mode_flag == True:

					if request_user != image_owner:

						if not request_user.is_superuser:

							message = 'CPW0370: ERROR! Attempting to Add an Image to a Collection for a different Owner: ' + str(image_owner) + '!'
							raise serializers.ValidationError(message)

		return True


	"""
		Collection Serializer, For an Image in a Cell within a Collection, Validate the supplied Server, Owner, Image Id and ROI ID Fields
	"""
	def validate_image_json(self, server_str, user, image_id, roi_id):

		server_list = server_str.split("@")

		server_uid = str(server_list[0])
		server_url = str(server_list[1])

		if exists_server_for_uid_url(server_uid, server_url):

			server = get_servers_for_uid_url(server_uid, server_url)

			if server.is_wordpress():

				if not self.validate_wordpress_image_id(server, user, image_id):

					message = 'CPW0380: ERROR! Image NOT Present on : ' + server_str + '!'
					raise serializers.ValidationError(message)

			else:

				if server.is_omero547() or server.is_omero56():

					if self.validate_imaging_image_id(server, user, image_id):

						if roi_id != 0:

							if not self.validate_roi_id(server, user, image_id, roi_id):

								message = 'CPW0390: ERROR! ROI ID ' + str(roi_id) + ', for Image ID ' + str(image_id) + ", NOT Present on : " + server_str + '!'
								raise serializers.ValidationError(message)
					else:

						message = 'CPW0400: ERROR! Image ID ' + str(image_id) + ', NOT Present on : ' + server_str + '!'
						raise serializers.ValidationError(message)
				else:

					message = 'CPW0410: ERROR! Server Type Unknown : ' + server_str + '!'
					raise serializers.ValidationError(message)

			return server

		else:

			message = 'CPW0420: ERROR! Server Unknown : ' + server_str + '!'
			raise serializers.ValidationError(message)

			return None


	"""
		Collection Serializer, For a WordPress Image in a Collection, Validate the supplied Server, Owner, Image Id Fields
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
		Collection Serializer, For an OMERO Image within a Colleciton, Check the supplied Image Exists
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
		Collection Serializer, For an OMERO Image within a Colleciton, Check the supplied Image ROI ID Exists
	"""
	def validate_roi_id(self, server, user, image_id, roi_id):

		data = server.check_imaging_server_image_roi(user, image_id, roi_id)

		json_roi = data['roi']
		roi_id = json_roi['id']

		if roi_id == "":
			return False
		else:
			return True
