#!/usr/bin/python3
###!
# \file         matrixserializer.py
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
# This Serializer provides Create, Read, Update and Delete functions for a Matrix (Bench)
###
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.db import models

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Image
from matrices.models import Server
from matrices.models import Credential

from matrices.routines import get_primary_wordpress_server
from matrices.routines import get_images_for_id_server_owner_roi
from matrices.routines import exists_image_for_id_server_owner_roi
from matrices.routines import exists_server_for_uid_url
from matrices.routines import get_servers_for_uid_url
from matrices.routines import get_credential_for_user

from matrices.serializers import CellSerializer


WORDPRESS_SUCCESS = 'Success!'

MAX_COLUMNS = 10000
MAX_ROWS = 10000
MIN_COLUMNS = 3
MIN_ROWS = 3
CONST_255 = 255
CONST_4095 = 4095
CONST_450 = 450
CONST_75 = 75
CONST_ZERO = 0


"""
	This Serializer provides Create, Read, Update and Delete functions for a Matrix (Bench)
"""
class MatrixSerializer(serializers.HyperlinkedModelSerializer):

	title = serializers.CharField(max_length=255, required=False, allow_blank=True)
	description = serializers.CharField(max_length=4095, required=False, allow_blank=True)
	height = serializers.IntegerField(required=False, default=75)
	width = serializers.IntegerField(required=False, default=75)

	owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

	bench_cells = CellSerializer(many=True, required=False)

	class Meta:
		model = Matrix
		fields = ('url', 'id', 'title', 'description', 'height', 'width', 'owner', 'bench_cells')
		read_only_fields = ('id', 'url', )


	"""
		Matrix Serializer, Create Method
	"""
	def create(self, validated_data):

		request_user = None

		request = self.context.get("request")

		if request and hasattr(request, "user"):

			request_user = request.user

		else:

			user_id = Token.objects.get(key=request.auth.key).user_id
			request_user = User.objects.get(id=user_id)


		if validated_data.get('title', None) == None and validated_data.get('description', None) == None and validated_data.get('bench_cells', None) == None:

			message = 'CPW0290: ERROR! NO data supplied for Bench Creation!'
			raise serializers.ValidationError(message)


		matrix_title = ""
		matrix_description = ""

		if validated_data.get('title', None) == None:

			matrix_title = ""

		else:

			matrix_title = validated_data.get('title')

		if validated_data.get('description', None) == None:

			matrix_description = ""

		else:

			matrix_description = validated_data.get('description')

		matrix_height = validated_data.get('height')
		matrix_width = validated_data.get('width')


		matrix_owner = validated_data.get('owner')

		if request_user != matrix_owner:

			if not request_user.is_superuser:

				message = 'CPW0030: ERROR! Attempting to Add a new Bench for a different Owner: ' + str(matrix_owner) + '!'
				raise serializers.ValidationError(message)

		matrix_blogpost = ''

		self.validate_matrix_json_fields(matrix_title, matrix_description, matrix_height, matrix_width)

		matrix = None

		cell_list = list()

		if validated_data.get('bench_cells', None) == None:

			matrix = Matrix.create(matrix_title, matrix_description, matrix_blogpost, matrix_height, matrix_width, matrix_owner)

			cell_title = ""
			cell_description = ""
			cell_xcoordinate = 0
			cell_ycoordinate = 0
			cell_blogpost = ''
			cell_image = None

			rows = 2
			columns = 2

			while cell_xcoordinate <= columns:

				cell_ycoordinate = 0

				while cell_ycoordinate <= rows:

					cell = Cell.create(matrix, cell_title, cell_description, cell_xcoordinate, cell_ycoordinate, cell_blogpost, cell_image)

					cell_list.append(cell)

					cell_ycoordinate = cell_ycoordinate + 1

				cell_xcoordinate = cell_xcoordinate + 1

		else:

			cells_data = validated_data.pop('bench_cells')

			create_flag = True

			self.validate_cells(cells_data, request_user, create_flag)

			matrix = Matrix.create(matrix_title, matrix_description, matrix_blogpost, matrix_height, matrix_width, matrix_owner)

			for cell_data in cells_data:

				cell_title = cell_data.get('title')
				cell_description = cell_data.get('description')
				cell_xcoordinate = cell_data.get('xcoordinate')
				cell_ycoordinate = cell_data.get('ycoordinate')

				cell_blogpost = ''

				image_data = cell_data.get('image')

				image = None

				if image_data is None:

					image = None

				else:

					if cell_title == '' and cell_description == '':

						message = 'CPW0050: ERROR! Attempting to Add an Image to a Bench WITHOUT a Title or Description!'
						raise serializers.ValidationError(message)

					image_server = image_data.get('server')
					image_owner = image_data.get('owner')
					image_id = image_data.get('image_id')
					image_roi_id = image_data.get('roi')

					server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id)

					image_identifier = int(image_id)

					image_name = ''
					image_viewer_url = ''
					image_birdseye_url = ''
					image_roi = 0

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


					if exists_image_for_id_server_owner_roi(image_id, server, image_owner, image_roi):

						existing_image_list = get_images_for_id_server_owner_roi(image_id, server, image_owner, image_roi)

						image = existing_image_list[0]

					else:

						image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_roi, image_owner)

						image.save()


				cell_in = Cell.create(matrix, cell_title, cell_description, cell_xcoordinate, cell_ycoordinate, cell_blogpost, image)

				cell_list.append(cell_in)


		credential = get_credential_for_user(request.user)

		post_id = ''

		if credential.has_apppwd():

			serverWordpress = get_primary_wordpress_server()

			returned_blogpost = serverWordpress.post_wordpress_post(request_user.username, matrix.title, matrix.description)

			if returned_blogpost['status'] == WORDPRESS_SUCCESS:

				post_id = returned_blogpost['id']

			else:

				message = "WordPress Error - Contact System Administrator : "  + str(returned_blogpost) + '!'
				raise serializers.ValidationError(message)


		matrix.set_blogpost(post_id)

		matrix.save()


		for cell_out in cell_list:

			cell_out.matrix = matrix

			post_id = ''

			if cell_out.image is not None:

				if credential.has_apppwd():

					serverWordpress = get_primary_wordpress_server()

					returned_blogpost = serverWordpress.post_wordpress_post(request_user.username, cell_out.title, cell_out.description)

					if returned_blogpost['status'] == WORDPRESS_SUCCESS:

						post_id = returned_blogpost['id']

					else:

						message = "WordPress Error - Contact System Administrator : "  + str(returned_blogpost) + '!'
						raise serializers.ValidationError(message)


			cell_out.set_blogpost(post_id)

			cell_out.save()

		return matrix


	"""
		Matrix Serializer, Update Method
	"""
	def update(self, instance, validated_data):

		request_user = None

		request = self.context.get("request")

		if request and hasattr(request, "user"):

			request_user = request.user

		else:

			user_id = Token.objects.get(key=request.auth.key).user_id
			request_user = User.objects.get(id=user_id)


		bench_title = validated_data.get('title', instance.title)
		bench_description = validated_data.get('description', instance.description)
		bench_height = validated_data.get('height', instance.height)
		bench_width = validated_data.get('width', instance.width)
		bench_owner = validated_data.get('owner', instance.owner)

		if request_user != bench_owner:

			if not request_user.is_superuser:

				message = 'CPW0070: ERROR! Attempting to Update an existing Bench for a different Owner: ' + str(bench_owner) + '!'
				raise serializers.ValidationError(message)


		self.validate_matrix_json_fields(bench_title, bench_description, bench_height, bench_width)


		if validated_data.get('bench_cells', None) == None:

			message = 'CPW0280: ERROR! No Cells Supplied for UPDATE!'
			raise serializers.ValidationError(message)

		cells_data = validated_data.pop('bench_cells')

		create_flag = False

		self.validate_cells(cells_data, request_user, create_flag)

		self.update_existing_cells(instance, request_user, cells_data)

		self.delete_missing_cells(instance, request_user, cells_data)

		self.add_new_cells(instance, request_user, cells_data)

		instance.title = bench_title
		instance.description = bench_description
		instance.height = bench_height
		instance.width = bench_width

		post_id = instance.blogpost

		if instance.blogpost == '' or instance.blogpost == '0':

			credential = get_credential_for_user(request.user)

			if credential.has_apppwd():

				serverWordpress = get_primary_wordpress_server()

				returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, instance.title, instance.description)

				if returned_blogpost['status'] == WORDPRESS_SUCCESS:

					post_id = returned_blogpost['id']

				else:

					message = "WordPress Error - Contact System Administrator : "  + str(returned_blogpost) + '!'
					raise serializers.ValidationError(message)

		instance.blogpost = post_id

		instance.save()

		return instance


	"""
		Matrix Serializer, For a Matrix, Update any Existing Cells from Input Grid
	"""
	def update_existing_cells(self, instance, request_user, cells_data):

		update_cell_list = list()

		bench_cells = (instance.bench_cells).all()
		bench_cells = list(bench_cells)

		for bench_cell in bench_cells:

			bench_cell_id = bench_cell.id
			bench_cell_title = bench_cell.title
			bench_cell_description = bench_cell.description
			bench_cell_xcoordinate = bench_cell.xcoordinate
			bench_cell_ycoordinate = bench_cell.ycoordinate

			update_flag = True

			for cell_data in cells_data:

				cell_id = cell_data.get('id', 0)
				cell_title = cell_data.get('title')
				cell_description = cell_data.get('description')
				cell_xcoordinate = cell_data.get('xcoordinate')
				cell_ycoordinate = cell_data.get('ycoordinate')

				image_data = cell_data.get('image')

				if cell_id == bench_cell_id:

					cell_image_data_id = 0
					bench_image_data_id = 0

					if image_data is None:

						cell_image_data_id = 0

					else:

						cell_image_data_id = image_data.get('id')

					if bench_cell.image is None:

						bench_image_data_id = 0

					else:

						bench_image_data_id = bench_cell.image.id

					if cell_title == bench_cell_title and cell_description == bench_cell_description and cell_xcoordinate == bench_cell_xcoordinate and cell_ycoordinate == bench_cell_ycoordinate and cell_image_data_id == bench_image_data_id:

						update_flag = False

					else:

						bench_cell.title = cell_title
						bench_cell.description = cell_description
						bench_cell.xcoordinate = cell_xcoordinate
						bench_cell.ycoordinate = cell_ycoordinate

						if image_data is not None and bench_cell.image is None:

							#update bench cell image with image_data

							image_server = image_data.get('server')
							image_owner = image_data.get('owner')
							image_id = image_data.get('image_id')
							image_roi_id = image_data.get('roi')

							server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id)

							image_identifier = int(image_id)

							image_name = ''
							image_viewer_url = ''
							image_birdseye_url = ''
							image_roi = 0

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


							if exists_image_for_id_server_owner_roi(image_id, server, image_owner, image_roi):

								existing_image_list = get_images_for_id_server_owner_roi(image_id, server, image_owner, image_roi)

								image = existing_image_list[0]

								bench_cell.image = image

							else:

								image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_roi, image_owner)

								image.save()

								bench_cell.image = image


							post_id = ''

							if not bench_cell.has_blogpost():

								credential = get_credential_for_user(request.user)

								if credential.has_apppwd():

									serverWordpress = get_primary_wordpress_server()

									returned_blogpost = serverWordpress.post_wordpress_post(request_user.username, bench_cell.title, bench_cell.description)

									if returned_blogpost['status'] == WORDPRESS_SUCCESS:

										post_id = returned_blogpost['id']

									else:

										message = "WordPress Error - Contact System Administrator : "  + str(returned_blogpost) + '!'
										raise serializers.ValidationError(message)

							bench_cell.set_blogpost(post_id)


						if image_data is not None and bench_cell.image is not None:

							#update bench cell image with image_data IF image_data is different
							#	Set bench cell image Active to True
							#	Set image data image Active to False

							image_server = image_data.get('server')
							image_owner = image_data.get('owner')
							image_id = image_data.get('image_id')
							image_roi_id = image_data.get('roi')

							image_identifier = int(image_id)

							if image_identifier != bench_cell.image.identifier:

								server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id)

								image_name = ''
								image_viewer_url = ''
								image_birdseye_url = ''
								image_roi = 0

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


								if exists_image_for_id_server_owner_roi(image_id, server, image_owner, image_roi):

									existing_image_list = existing_image_list = get_images_for_id_server_owner_roi(image_id, server, image_owner, image_roi)

									image = existing_image_list[0]

									image.save()

									bench_cell.image = image

								else:

									image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_roi, image_owner)

									image.save()

									bench_cell.image = image


								post_id = ''

								if bench_cell.has_blogpost():

									credential = get_credential_for_user(request.user)

									if credential.has_apppwd():

										serverWordpress = get_primary_wordpress_server()

										response = serverWordpress.delete_wordpress_post(request_user.username, bench_cell.blogpost)

										if response != WORDPRESS_SUCCESS:

											message = "WordPress Error - Contact System Administrator : "  + str(returned_blogpost) + '!'
											raise serializers.ValidationError(message)

										returned_blogpost = serverWordpress.post_wordpress_post(request_user.username, bench_cell.title, bench_cell.description)

										if returned_blogpost['status'] == WORDPRESS_SUCCESS:

											post_id = returned_blogpost['id']

										else:

											message = "WordPress Error - Contact System Administrator : "  + str(returned_blogpost) + '!'
											raise serializers.ValidationError(message)

								bench_cell.set_blogpost(post_id)


						if image_data is None and bench_cell.image is not None:

							bench_cell.image = None

							if bench_cell.has_blogpost():

								credential = get_credential_for_user(request.user)

								if credential.has_apppwd():

									serverWordpress = get_primary_wordpress_server()

									response = serverWordpress.delete_wordpress_post(request_user.username, bench_cell.blogpost)

									if response != WORDPRESS_SUCCESS:

										message = "WordPress Error - Contact System Administrator : "  + str(returned_blogpost) + '!'
										raise serializers.ValidationError(message)

							bench_cell.set_blogpost('')


						update_cell_list.append(bench_cell)


		for update_cell in update_cell_list:

			update_cell.save()


	"""
		Matrix Serializer, For a Matrix, Delete any Missing Cells from Input Grid
	"""
	def delete_missing_cells(self, instance, request_user, cells_data):

		delete_cell_list = list()

		bench_cells = (instance.bench_cells).all()
		bench_cells = list(bench_cells)

		for bench_cell in bench_cells:

			bench_cell_id = bench_cell.id

			delete_flag = True

			for cell_data in cells_data:

				cell_id = cell_data.get('id', 0)

				if cell_id == bench_cell_id:

					delete_flag = False

			if delete_flag == True:

				delete_cell_list.append(bench_cell)


		for delete_cell in delete_cell_list:

			if delete_cell.has_blogpost():

				credential = get_credential_for_user(request.user)

				if credential.has_apppwd():

					serverWordpress = get_primary_wordpress_server()

					response = serverWordpress.delete_wordpress_post(request_user.username, delete_cell.blogpost)

					if response != WORDPRESS_SUCCESS:

						message = "WordPress Error - Contact System Administrator!"
						raise serializers.ValidationError(message)


			delete_cell.delete()


	"""
		Matrix Serializer, For a Matrix, Add New Cells
	"""
	def add_new_cells(self, instance, request_user, cells_data):

		for cell_data in cells_data:

			cell_id = cell_data.get('id', 0)
			cell_title = cell_data.get('title')
			cell_description = cell_data.get('description')
			cell_xcoordinate = cell_data.get('xcoordinate')
			cell_ycoordinate = cell_data.get('ycoordinate')
			cell_blogpost = "0"

			cell_image = None

			"""
				Add NEW CELLS
			"""
			if cell_id == 0:

				image_data = cell_data.pop('image')

				if image_data is None:

					cell_image = None

				else:

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


					if exists_image_for_id_server_owner_roi(image_id, server, image_owner, image_roi):

						existing_image_list = get_images_for_id_server_owner_roi(image_id, server, image_owner, image_roi)

						existing_image = existing_image_list[0]

						cell_image = existing_image

					else:

						cell_image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_roi, owner)

						cell_image.save()


					post_id = ''

					credential = get_credential_for_user(request.user)

					if credential.has_apppwd():

						serverWordpress = get_primary_wordpress_server()

						returned_blogpost = serverWordpress.post_wordpress_post(request_user.username, cell_title, cell_description)

						if returned_blogpost['status'] == WORDPRESS_SUCCESS:

							post_id = returned_blogpost['id']

						else:

							message = "WordPress Error - Contact System Administrator : "  + str(returned_blogpost) + '!'
							raise serializers.ValidationError(message)

					cell_blogpost = post_id


				cell = Cell.create(instance, cell_title, cell_description, cell_xcoordinate, cell_ycoordinate, cell_blogpost, cell_image)

				cell.save()


	"""
		Matrix Serializer, For a Matrix, Validate the supplied Title, Description, Height and Width fields
	"""
	def validate_matrix_json_fields(self, title, description, height, width):

		len_title = len(title)
		len_description = len(description)

		"""
			Title and Description field overflows are trapped by the Django REST framework,
			 so these next 2 checks are redundant
		"""
		if len_title > CONST_255:

			message = 'CPW0130: ERROR! Bench Title Length (' + str(len_title) + ') is greater than 255!'
			raise serializers.ValidationError(message)

		if len_description > CONST_4095:

			message = 'CPW0120: ERROR! Bench Description Length (' + str(len_title) + ') is greater than 4095!'
			raise serializers.ValidationError(message)

		if height > CONST_450:

			message = 'CPW0080: ERROR! Bench Cell Height (' + str(height) + ') is greater than 450!'
			raise serializers.ValidationError(message)

		if height < CONST_75:

			message = 'CPW0090: ERROR! Bench Cell Height (' + str(height) + ') is less than 75!'
			raise serializers.ValidationError(message)

		if width > CONST_450:

			message = 'CPW0100: ERROR! Bench Cell Width (' + str(width) + ') is greater than 450!'
			raise serializers.ValidationError(message)

		if width < CONST_75:

			message = 'CPW0110: ERROR! Bench Cell Width (' + str(width) + ') is less than 75!'
			raise serializers.ValidationError(message)


	"""
		Matrix Serializer, For a Matrix, Validate the supplied Cells
	"""
	def validate_cells(self, cells_data, request_user, mode_flag):

		maxX = 0
		maxY = 0

		if not cells_data:
			message = 'CPW0190: ERROR! NO Cells supplied with Bench!'
			raise serializers.ValidationError(message)

		for cell_data in cells_data:

			title = cell_data.get('title')
			description = cell_data.get('description')

			self.validate_cell_json_fields(title, description)

			currX = int(cell_data.get('xcoordinate', 0))
			currY = int(cell_data.get('ycoordinate', 0))

			if currX > maxX:
				maxX = currX

			if currY > maxY:
				maxY = currY

		max_column_index = maxX
		max_row_index = maxY

		maxX += 1
		maxY += 1

		if maxX > MAX_COLUMNS:
			message = 'CPW0240: ERROR! Too many Columns in Bench (' + str(maxX) + '); No more than 10,000 Columns allowed!'
			raise serializers.ValidationError(message)

		if maxY > MAX_ROWS:
			message = 'CPW0250: ERROR! Too many Rows in Bench (' + str(maxY) + '); No more than 10,000 Rows allowed!'
			raise serializers.ValidationError(message)

		if maxX < MIN_COLUMNS:
			message = 'CPW0220: ERROR! Too few Columns in Bench (' + str(maxX) + '); At least 3 Columns required!'
			raise serializers.ValidationError(message)

		if maxY < MIN_ROWS:
			message = 'CPW0230: ERROR! Too few Rows in Bench (' + str(maxY) + '); At least 3 Rows required!'
			raise serializers.ValidationError(message)

		bench_cells=[[0 for cc in range(maxY)] for rc in range(maxX)]

		i = 0

		while i < maxX:

			j = 0

			while j < maxY:

				bench_cells[i][j] = False
				j += 1

			i += 1

		cnt = 0

		for cell_data in cells_data:

			cnt += 1

			i = cell_data.get('xcoordinate', 0)
			j = cell_data.get('ycoordinate', 0)

			if bench_cells[i][j] == True:
				message = 'CPW0160: ERROR! Duplicate Cell : Column Index = ' + str(i) + ', Row Index = ' + str(j) + '!'
				raise serializers.ValidationError(message)

			bench_cells[i][j] = True

		i = 0

		cnt = 0

		while i < maxX:

			j = 0

			while j < maxY:

				cnt += 1

				if bench_cells[i][j] == False:
					message = 'CPW0180: ERROR! Missing Cell : Column Index = ' + str(i) + ', Row Index = ' + str(j) + '!'
					raise serializers.ValidationError(message)

				j += 1

			i += 1


		for cell_data in cells_data:

			image_data = cell_data.get('image')

			xcoordinate = cell_data.get('xcoordinate', 0)
			ycoordinate = cell_data.get('ycoordinate', 0)
			cell_title = cell_data.get('title')
			cell_description = cell_data.get('description')

			if xcoordinate == CONST_ZERO and image_data is not None:
				message = 'CPW0010: ERROR! An Image is not Permitted in : Column Index = ' + str(xcoordinate) + '!'
				raise serializers.ValidationError(message)

			if xcoordinate == max_column_index and image_data is not None:
				message = 'CPW0015: ERROR! An Image is not Permitted in : Column Index = ' + str(xcoordinate) + '!'
				raise serializers.ValidationError(message)

			if ycoordinate == CONST_ZERO and image_data is not None:
				message = 'CPW0020: ERROR! An Image is not Permitted in : Row Index = ' + str(ycoordinate) + '!'
				raise serializers.ValidationError(message)

			if ycoordinate == max_row_index and image_data is not None:
				message = 'CPW0025: ERROR! An Image is not Permitted in : Row Index = ' + str(ycoordinate) + '!'
				raise serializers.ValidationError(message)

			if image_data is not None:

				server = image_data.get('server')
				image_owner = image_data.get('owner')
				image_id = image_data.get('image_id')
				roi_id = image_data.get('roi')

				if mode_flag == True:

					if request_user != image_owner:

						if not request_user.is_superuser:

							message = 'CPW0060: ERROR! Attempting to Add an Image to a Bench for a different Owner: ' + str(image_owner) + '!'
							raise serializers.ValidationError(message)

				if cell_title == '' or cell_description == '':

					message = 'CPW0055: ERROR! Attempting to Add an Image to a Bench WITHOUT a Title or Description!'
					raise serializers.ValidationError(message)


				server = self.validate_image_json(server, image_owner, image_id, roi_id)

		return True


	"""
		Matrix Serializer, For a Cell in a Matrix, Validate the supplied Title and Description fields
	"""
	def validate_cell_json_fields(self, title, description):

		len_title = len(title)
		len_description = len(description)

		"""
			Title and Description field overflows are trapped by the Django REST framework,
			 so these next 2 checks are redundant
		"""
		if len_title > CONST_255:

			message = 'CPW0150: ERROR! Cell Title Length (' + str(len_title) + ') is greater than 255!'
			raise serializers.ValidationError(message)

		if len_description > CONST_4095:

			message = 'CPW0140: ERROR! Cell Description Length (' + str(len_title) + ') is greater than 4095!'
			raise serializers.ValidationError(message)


	"""
		Matrix Serializer, For an Image in a Cell within a Matrix, Validate the supplied Server, Owner, Image Id and ROI ID Fields
	"""
	def validate_image_json(self, server_str, user, image_id, roi_id):

		server_list = server_str.split("@")

		server_uid = str(server_list[0])
		server_url = str(server_list[1])

		if exists_server_for_uid_url(server_uid, server_url):

			server = get_servers_for_uid_url(server_uid, server_url)

			print("server : " + str(server))

			if server.is_wordpress():

				if not self.validate_wordpress_image_id(server, user, image_id):

					message = 'CPW0265: ERROR! Image NOT Present on : ' + server_str + '!'
					raise serializers.ValidationError(message)
			else:

				if server.is_omero547() or server.is_omero56():

					if self.validate_imaging_image_id(server, user, image_id):

						if roi_id != 0:

							if not self.validate_roi_id(server, user, image_id, roi_id):

								message = 'CPW0205: ERROR! ROI ID ' + str(roi_id) + ', for Image ID ' + str(image_id) + ", NOT Present on : " + server_str + '!'
								raise serializers.ValidationError(message)
					else:

						message = 'CPW0175: ERROR! Image ID ' + str(image_id) + ', NOT Present on : ' + server_str + '!'
						raise serializers.ValidationError(message)
				else:

					message = 'CPW0275: ERROR! Server Type Unknown : ' + server_str + '!'
					raise serializers.ValidationError(message)

			return server

		else:

			message = 'CPW0215: ERROR! Server Unknown : ' + server_str + '!'
			raise serializers.ValidationError(message)

			return None


	"""
		Matrix Serializer, For an Image in a Cell within a Matrix, Validate the supplied Server, Owner, Image Id and ROI ID Fields
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
		Matrix Serializer, For an OMERO Image in a Cell within a Matrix, Check the supplied Image Exists
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
		Matrix Serializer, For an OMERO Image in a Cell within a Matrix, Check the supplied Image ROI ID Exists
	"""
	def validate_roi_id(self, server, user, image_id, roi_id):

		data = server.check_imaging_server_image_roi(user, image_id, roi_id)

		json_roi = data['roi']
		roi_id = json_roi['id']

		if roi_id == "":
			return False
		else:
			return True
