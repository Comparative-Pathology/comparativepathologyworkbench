#!/usr/bin/python3
#
# ##
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
# ##
#
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Image
from matrices.models import Collection

from matrices.routines import exists_active_collection_for_user
from matrices.routines import exists_collection_for_image
from matrices.routines import exists_image_for_id_server_owner_roi
from matrices.routines import exists_server_for_uid_url
from matrices.routines import exists_user_for_username
from matrices.routines import get_active_collection_for_user
from matrices.routines import get_credential_for_user
from matrices.routines import get_images_for_id_server_owner_roi
from matrices.routines import get_servers_for_uid_url
from matrices.routines import get_user_from_username
from matrices.routines import get_primary_cpw_environment

from matrices.serializers import CellSerializer


WORDPRESS_SUCCESS = 'Success!'

CONST_255 = 255
CONST_4095 = 4095
CONST_450 = 450
CONST_75 = 75
CONST_ZERO = 0


class MatrixSerializer(serializers.HyperlinkedModelSerializer):
    """A Serializer of Benches

    A Serializer of Benches in the Comparative Pathology Workbench REST Interface

    This Serializer provides Create, Read and Update functions for a Bench

    Parameters:
        id(Read Only):      The (internal) Id of the Image.
        url(Read Only):     The (internal) URL of the Image.
        owner:              The Owner (User Model) of the Image.
        title:              The Title of the Bench, Maximum 255 Characters.
        description:        The Description of the Bench, Maximum 4095 Characters.
        height:             The Height in Pixels of the Cells in this Bench, an Integer, between 75 and 450.
        width:              The Width in Pixels of the Cells in this Bench, an Integer, between 75 and 450.
        bench_cells:        An array of cells data.

    """

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

    def create(self, validated_data):
        """Create Method.

        Process the supplied Bench JSON and create a new Bench.

        Parameters:
            validated_data:     The validated JSON Bench data.

        Returns:
            None

        Raises:
            ValidationError:
                CPW_REST:0370 - No Cells supplied in validated data
            ValidationError:
                CPW_REST:0050 - Attempting to Add a Bench for a Different Owner
            ValidationError:
                CPW_REST:0070 - Attempting to Add a Image without a Cell Title or Description
            ValidationError:
                WordPress Error

        """

        request_user = None

        # Get the request
        request = self.context.get("request")

        # Is there a User request attribute?
        if request and hasattr(request, "user"):

            request_user = request.user

        # No
        else:

            # Get the User Id from the supplied Token
            user_id = Token.objects.get(key=request.auth.key).user_id
            # Get the User Object from the User Id
            request_user = User.objects.get(id=user_id)

        # Do we have any Bench Attributes?
        if validated_data.get('title', None) is None and \
           validated_data.get('description', None) is None and \
           validated_data.get('bench_cells', None) is None:

            # No, then Raise an Error!
            message = 'CPW_REST:0370 ERROR! NO data supplied for Bench Creation!'
            raise serializers.ValidationError(message)

        matrix_title = ""
        matrix_description = ""

        # Access the Bench Title Attribute
        if validated_data.get('title', None) is None:

            matrix_title = ""

        else:

            matrix_title = validated_data.get('title')

        # Access the Bench Description Attribute
        if validated_data.get('description', None) is None:

            matrix_description = ""

        else:

            matrix_description = validated_data.get('description')

        # Access the Bench Height Attribute
        matrix_height = validated_data.get('height')
        # Access the Bench Width Attribute
        matrix_width = validated_data.get('width')

        # Access the Bench Owner Attribute
        matrix_owner = validated_data.get('owner')

        # Is the Request User different to the Bench Owner?
        if request_user != matrix_owner:

            # Yes, Is the Request User a Superuser?
            if not request_user.is_superuser:

                # No, then Raise an Error!
                message = 'CPW_REST:0050 ERROR! Attempting to Add a new Bench for a different Owner: ' + \
                          str(matrix_owner) + '!'
                raise serializers.ValidationError(message)

        matrix_blogpost = ''

        # Validate the supplied Bench JSON Fields
        self.validate_matrix_json_fields(matrix_title, matrix_description, matrix_height, matrix_width)

        matrix = None

        cell_list = list()

        # Do we have any Cells supplied?
        if validated_data.get('bench_cells', None) is not None:

            # Get the Cells JSON Data
            cells_data = validated_data.get('bench_cells', None)

            if cells_data == []:

                # No, we need to set up a Default Bench 
                #  Create a Matrix Object
                matrix = Matrix.create(matrix_title,
                                       matrix_description,
                                       matrix_blogpost,
                                       matrix_height,
                                       matrix_width,
                                       matrix_owner)

                # Define Cell Attributes
                cell_title = ""
                cell_description = ""
                cell_xcoordinate = 0
                cell_ycoordinate = 0
                cell_blogpost = ''
                cell_image = None

                # We will set up a default 3 x 3 Matrix
                rows = 2
                columns = 2

                # While the X Coordinate is less than 2
                while cell_xcoordinate <= columns:

                    cell_ycoordinate = 0

                    # While the Y Coordinate is less than 2
                    while cell_ycoordinate <= rows:

                        # Create a Default Cell Object
                        cell = Cell.create(matrix,
                                           cell_title,
                                           cell_description,
                                           cell_xcoordinate,
                                           cell_ycoordinate,
                                           cell_blogpost,
                                           cell_image)

                        # Add this default cell to the list of cells to be added
                        cell_list.append(cell)

                        # Increment the Row Count
                        cell_ycoordinate = cell_ycoordinate + 1

                    # Increment the Column Count
                    cell_xcoordinate = cell_xcoordinate + 1

            else:

                # Creation mode
                create_flag = True

                # Validate the supplied Cells ... 
                self.validate_cells(cells_data, request_user, create_flag)

                #  Create a Matrix Object
                matrix = Matrix.create(matrix_title,
                                       matrix_description,
                                       matrix_blogpost,
                                       matrix_height,
                                       matrix_width,
                                       matrix_owner)

                # Process each Cell in the Cells Data
                for cell_data in cells_data:

                    # Get the Cell Attributes
                    cell_title = cell_data.get('title')
                    cell_description = cell_data.get('description')
                    cell_xcoordinate = cell_data.get('xcoordinate')
                    cell_ycoordinate = cell_data.get('ycoordinate')

                    cell_blogpost = ''

                    # Get the Image Data from the Cell Data
                    image_data = cell_data.get('image')

                    image = None

                    # Is there an Image for this Cell?
                    if image_data is None:

                        # No image
                        image = None

                    # Yes
                    else:

                        # Are Both the Cell Title and Description Empty?
                        if cell_title == '' and cell_description == '':

                            # Yes, Raise an Error!
                            message = 'CPW_REST:0070 ERROR! Attempting to Add an Image to a Bench WITHOUT a Title ' + \
                                      'or Description!'
                            raise serializers.ValidationError(message)

                        # Get the mage Attributes
                        image_server = image_data.get('server')
                        owner = image_data.get('owner')
                        image_id = image_data.get('image_id')
                        image_roi_id = image_data.get('roi')
                        image_comment = image_data.get('comment')
                        image_hidden = False

                        # Get the Image Owner Object
                        image_owner = get_user_from_username(owner)

                        # Validate the Image Attributes and return the associated Image Server
                        server = self.validate_image_json(image_server,
                                                          image_owner,
                                                          image_id,
                                                          image_roi_id,
                                                          image_comment)

                        # Set up further Image Attributes
                        image_name = ''
                        image_viewer_url = ''
                        image_birdseye_url = ''
                        image_roi = 0

                        # Is the Image Server a WordPress Server
                        if server.is_wordpress():

                            # Check and Retrieve the Image Data from the Server
                            data = server.check_wordpress_image(image_owner, image_id)

                            json_image = data['image']

                            # Update the further Image Attributes
                            image_name = json_image['name']
                            image_viewer_url = json_image['viewer_url']
                            image_birdseye_url = json_image['birdseye_url']

                        # Is the Image Server an OMERO Server
                        else:

                            # Check and Retrieve the Image Data from the Server
                            data = server.check_imaging_server_image(image_id)

                            json_image = data['image']

                            # Update the further Image Attributes
                            image_name = json_image['name']
                            image_viewer_url = json_image['viewer_url']
                            image_birdseye_url = json_image['birdseye_url']

                            # Do we have an ROI id?
                            if image_roi_id != 0:

                                # Yes, Check and Retrieve ROI Data from the Server
                                data = server.check_imaging_server_image_roi(image_id, image_roi_id)

                                json_roi = data['roi']

                                # Update the further Image ROI Attribute
                                image_roi = int(json_roi['id'])

                        # Does the Image already exist in the Database?
                        #  Yes
                        if exists_image_for_id_server_owner_roi(image_id, server, image_owner, image_roi):

                            # Get the Existing Image
                            existing_image_list = get_images_for_id_server_owner_roi(image_id,
                                                                                     server,
                                                                                     image_owner,
                                                                                     image_roi)

                            image = existing_image_list[0]

                            # Is the requesting user Hiding Images in their Collections?
                            #  Yes - ste the Image Hidden flags to true
                            if request_user.profile.is_hide_collection_image():

                                image.set_hidden(True)
                                image.save()

                        # No ... 
                        else:

                            # Create a New Image Object
                            image = Image.create(image_id,
                                                 image_name,
                                                 server,
                                                 image_viewer_url,
                                                 image_birdseye_url,
                                                 image_roi,
                                                 image_owner,
                                                 image_comment,
                                                 image_hidden)

                            # Is the requesting user Hiding Images in their Collections?
                            #  Yes - ste the Image Hidden flags to true
                            if request_user.profile.is_hide_collection_image():

                                image.set_hidden(True)

                            # Save the New Object to the Database
                            image.save()

                        collection = None

                        # Does the Requesting User have a Active Collection?
                        if exists_active_collection_for_user(request_user):

                            # Get the Active Collection
                            collection = get_active_collection_for_user(request_user)

                        # No ...
                        else:

                            # Set up Attributes for a New Collection            
                            collection_title = "A Default REST Collection"
                            collection_description = "A Collection created by a REST Request"
                            collection_owner = request_user

                            # Create a New Collection Object
                            collection = Collection.create(collection_title,
                                                           collection_description,
                                                           collection_owner)
                            # Write the New Collection Object to the Database
                            collection.save()

                            # Set the New Collection to Requesting Users Active Collection
                            request_user.profile.set_active_collection(collection)
                            # Update the Database with the updated User.
                            request_user.save()

                        # If the Image is Not already in the Collection
                        if not exists_collection_for_image(collection, image):

                            # Add the Image to the Collection
                            Collection.assign_image(image, collection)

                    # Create a new Cell Object
                    cell_in = Cell.create(matrix,
                                          cell_title,
                                          cell_description,
                                          cell_xcoordinate,
                                          cell_ycoordinate,
                                          cell_blogpost,
                                          image)

                    # Add the new Cell Object to the Cell List
                    cell_list.append(cell_in)

        # Get the Primary Blogging Engine
        environment = get_primary_cpw_environment()

        # Get the Credentials for Requesting User
        credential = get_credential_for_user(request.user)

        post_id = ''

        # Does the Credential have a Password
        if credential.has_apppwd() and environment.is_wordpress_active():

            # Post a New Blogpost for the Bench
            returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                     matrix.title,
                                                                     matrix.description)

            # Check the Post Response
            if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                post_id = returned_blogpost['id']

            else:

                # If failure, Raise an Error!
                message = "WordPress Error - Contact System Administrator : " + str(returned_blogpost) + '!'
                raise serializers.ValidationError(message)

        # Update the Bench with the BlogPost Id
        matrix.set_blogpost(post_id)

        # Process the Cells to be added
        for cell_out in cell_list:

            # Set the Cell's Bench 
            cell_out.matrix = matrix

            post_id = ''

            # Does the Cell have an Image?
            if cell_out.image is not None:

                # Yes ... 
                #  Does the Credential have a Password
                if credential.has_apppwd() and environment.is_wordpress_active():

                    # Post a New Blogpost for the Cell
                    returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                             cell_out.title,
                                                                             cell_out.description)

                    # Check the Post Response
                    if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                        post_id = returned_blogpost['id']

                    else:

                        # If failure, Raise an Error!
                        message = "WordPress Error - Contact System Administrator : " + str(returned_blogpost) + '!'
                        raise serializers.ValidationError(message)

            # Update the Cell with the BlogPost Id
            cell_out.set_blogpost(post_id)

        # Update the Database with the Bench Object
        matrix.save()

        # Update the Database with the Cell Objects
        #  Process the Cells to be added
        for cell_out in cell_list:

            # Update the Database with the Cell Object
            cell_out.save()

        return matrix

    def update(self, instance, validated_data):
        """Update Method.

        Process the supplied Bench JSON and update the matching Existing Bench.

        Parameters:
            instance:           The Bench which will be added.
            validated_data:     The validated JSON Bench data.

        Returns:
            None

        Raises:
            ValidationError:
                CPW_REST:0100 - Attempting to Update a Bench for a Different Owner
            ValidationError:
                CPW_REST:0360 - No Cells supplied in validated data
            ValidationError:
                WordPress Error

        """

        request_user = None

        # Get the request
        request = self.context.get("request")

        # Is there a User request attribute?
        if request and hasattr(request, "user"):

            request_user = request.user

        # No
        else:

            # Get the User Id from the supplied Token
            user_id = Token.objects.get(key=request.auth.key).user_id
            # Get the User Object from the User Id
            request_user = User.objects.get(id=user_id)

        # Get the Bench Attributes
        bench_title = validated_data.get('title', instance.title)
        bench_description = validated_data.get('description', instance.description)
        bench_height = validated_data.get('height', instance.height)
        bench_width = validated_data.get('width', instance.width)
        bench_owner = validated_data.get('owner', instance.owner)

        # Is the Request User different to the Bench Owner?
        if request_user != bench_owner:

            # Yes, Is the Request User a Superuser?
            if not request_user.is_superuser:

                # No, then Raise an Error!
                message = 'CPW_REST:0100 ERROR! Attempting to Update an existing Bench for a different Owner: ' + \
                    str(bench_owner) + '!'
                raise serializers.ValidationError(message)

        # Validate the supplied Bench JSON Fields
        self.validate_matrix_json_fields(bench_title, bench_description, bench_height, bench_width)

        # Has any Cell Data been supplied?
        if validated_data.get('bench_cells', None) is None:

            # No, then Raise an Error!
            message = 'CPW_REST:0360 ERROR! No Cells Supplied for UPDATE!'
            raise serializers.ValidationError(message)

        # Get the Cell JSON Data
        cells_data = validated_data.pop('bench_cells')

        # Update Mode
        create_flag = False

        # Validate the supplied Cells ... 
        self.validate_cells(cells_data, request_user, create_flag)

        # Update any Existing Cells
        self.update_existing_cells(instance, request_user, cells_data)

        # Delete any Missing Cells
        self.delete_missing_cells(instance, request_user, cells_data)

        # Add any New Cells
        self.add_new_cells(instance, request_user, cells_data)

        # Update the Bench Attributes
        instance.title = bench_title
        instance.description = bench_description
        instance.height = bench_height
        instance.width = bench_width

        post_id = instance.blogpost

        # Does the Bench have a Blog Post?
        if instance.has_no_blogpost():

            # Get the Credentials for Requesting User
            credential = get_credential_for_user(request.user)

            # Get the Primary Blogging Engine
            environment = get_primary_cpw_environment()

            # Does the Credential have a Password
            if credential.has_apppwd() and environment.is_wordpress_active():

                # Post a New Blogpost
                returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                         instance.title,
                                                                         instance.description)

                # Check the Post Response
                if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                    post_id = returned_blogpost['id']

                else:

                    # If failure, Raise an Error!
                    message = "WordPress Error - Contact System Administrator : " + str(returned_blogpost) + '!'
                    raise serializers.ValidationError(message)

        instance.blogpost = post_id

        # Update the Bench
        instance.save()

        return instance

    def update_existing_cells(self, an_instance, a_request_user, a_cells_data):
        """Update the Existing Cells in the Bench

        Process the supplied Cells and Delete them from the Bench.

        Parameters:
            an_instance:        The Bench to which the Cells will be Deleted.
            a_request_user:     The Requesting User.
            a_cells_data:       The supplied array of Cells JSON.

        Returns:
            None

        Raises:
            ValidationError:
                WordPress Error

        """

        update_cell_list = list()

        # Get the Existing Cells associated with this Bench
        bench_cells = (an_instance.bench_cells).all()
        # Convert the QuerySet to a List
        bench_cells = list(bench_cells)

        # Process the Exising Bench Cells
        for bench_cell in bench_cells:

            # Get the Cell Attributes from the database
            bench_cell_id = bench_cell.id
            bench_cell_title = bench_cell.title
            bench_cell_description = bench_cell.description
            bench_cell_xcoordinate = bench_cell.xcoordinate
            bench_cell_ycoordinate = bench_cell.ycoordinate

            update_flag = True

            # Process the supplied cells data for each existing database cell
            for cell_data in a_cells_data:

                # Get the Supplied Cell Attributes from the JSON 
                cell_id = cell_data.get('id', 0)
                cell_title = cell_data.get('title')
                cell_description = cell_data.get('description')
                cell_xcoordinate = cell_data.get('xcoordinate')
                cell_ycoordinate = cell_data.get('ycoordinate')

                # Get the Supplied Cell Image Data
                image_data = cell_data.get('image')

                # If the Database Cell matches the Supplied JSON Cell
                if cell_id == bench_cell_id:

                    cell_image_data_id = 0
                    bench_image_data_id = 0

                    # If there is No Supplied Image Data
                    if image_data is None:

                        cell_image_data_id = 0

                    # If there is Supplied Image Data
                    else:

                        # Get the Supplied Image Id
                        cell_image_data_id = image_data.get('id')

                    # If there is No Database Image
                    if bench_cell.image is None:

                        bench_image_data_id = 0

                    # If there is Database Image
                    else:

                        # Get the Database Image Id
                        bench_image_data_id = bench_cell.image.id

                    # Compare ALL Supplied and Database Attributes
                    if cell_title == bench_cell_title and \
                       cell_description == bench_cell_description and \
                       cell_xcoordinate == bench_cell_xcoordinate and \
                       cell_ycoordinate == bench_cell_ycoordinate and \
                       cell_image_data_id == bench_image_data_id:

                        update_flag = False

                    # Supplied Attributes are different, use them!
                    else:

                        # Set the Bench Attributes to the Supplied Attributes
                        bench_cell.title = cell_title
                        bench_cell.description = cell_description
                        bench_cell.xcoordinate = cell_xcoordinate
                        bench_cell.ycoordinate = cell_ycoordinate

                        # If there was NO Database Image and there is a Supplied Image
                        if image_data is not None and bench_cell.image is None:

                            # Extract the supplied Image Attributes
                            image_server = image_data.get('server')
                            owner = image_data.get('owner')
                            image_id = image_data.get('image_id')
                            image_roi_id = image_data.get('roi')
                            image_comment = image_data.get('comment')

                            # Get the User Object for the Supplied Owner
                            image_owner = get_user_from_username(owner)

                            # Validate the Supplied Image Attributes, and return the Associated Server
                            server = self.validate_image_json(image_server,
                                                              image_owner,
                                                              image_id,
                                                              image_roi_id,
                                                              image_comment)

                            image_identifier = int(image_id)

                            image_name = ''
                            image_viewer_url = ''
                            image_birdseye_url = ''
                            image_roi = 0
                            image_hidden = False

                            # Is the Server a WordPress Server?
                            if server.is_wordpress():

                                # Get the Image from the WordPress Server for the supplied Id
                                data = server.check_wordpress_image(image_owner, image_id)

                                json_image = data['image']

                                # Extract the Server Image Attributes
                                image_name = json_image['name']
                                image_viewer_url = json_image['viewer_url']
                                image_birdseye_url = json_image['birdseye_url']

                            # Is the Server an OMERO Server?
                            else:

                                # Get the Image from the OMERO Server for the supplied Id
                                data = server.check_imaging_server_image(image_id)

                                json_image = data['image']

                                # Extract the Server Image Attributes
                                image_name = json_image['name']
                                image_viewer_url = json_image['viewer_url']
                                image_birdseye_url = json_image['birdseye_url']

                                # Is there an ROI Suppied too?
                                if image_roi_id != 0:

                                    # Get the Image ROI from the OMERO Server for the Supplied Roi Id
                                    data = server.check_imaging_server_image_roi(image_id, image_roi_id)

                                    json_roi = data['roi']

                                    # Extract the ROI Id
                                    image_roi = int(json_roi['id'])

                            image = None

                            # Does the Image already exist in the Database?
                            #  Yes
                            if exists_image_for_id_server_owner_roi(image_id, server, image_owner, image_roi):

                                # Get the Existing Image
                                existing_image_list = get_images_for_id_server_owner_roi(image_id,
                                                                                         server,
                                                                                         image_owner,
                                                                                         image_roi)

                                image = existing_image_list[0]

                                # Do we have a new Image comment
                                #  Yes
                                if image.comment != image_comment:

                                    # Set the Image Comment
                                    image.comment = image_comment

                                    # Update the Database
                                    image.save()

                                # Is the requesting user Hiding Images in their Collections?
                                #  Yes ...
                                if a_request_user.profile.is_hide_collection_image():

                                    #  Set the Image Hidden flags to true
                                    image.set_hidden(True)

                                    # Update the Database
                                    image.save()

                                # Associate the Cell with the Existing Image
                                bench_cell.image = image

                            # No ... 
                            else:

                                # Create a New Image Object
                                image = Image.create(image_id,
                                                     image_name,
                                                     server,
                                                     image_viewer_url,
                                                     image_birdseye_url,
                                                     image_roi,
                                                     image_owner,
                                                     image_comment,
                                                     image_hidden)

                                # Is the requesting user Hiding Images in their Collections?
                                #  Yes ...
                                if a_request_user.profile.is_hide_collection_image():

                                    #  Set the Image Hidden flags to true
                                    image.set_hidden(True)

                                # Save the New Object to the Database
                                image.save()

                                # Associate the Cell with the New Image
                                bench_cell.image = image

                            collection = None

                            # Does the Requesting User have a Active Collection?
                            if exists_active_collection_for_user(a_request_user):

                                # Get the Active Collection
                                collection = get_active_collection_for_user(a_request_user)

                            # No ...
                            else:

                                # Set up Attributes for a New Collection            
                                collection_title = "A Default REST Collection"
                                collection_description = "A Collection created by a REST Request"
                                collection_owner = a_request_user

                                # Create a New Collection Object
                                collection = Collection.create(collection_title,
                                                               collection_description,
                                                               collection_owner)
                                # Write the New Collection Object to the Database
                                collection.save()

                                # Set the New Collection to Requesting Users Active Collection
                                a_request_user.profile.set_active_collection(collection)
                                # Update the Database with the updated User.
                                a_request_user.save()

                            # If the Image is Not already in the Collection
                            if not exists_collection_for_image(collection, image):

                                # Add the Image to the Collection
                                Collection.assign_image(image, collection)

                            post_id = ''

                            # If the Cell has No BLogpost
                            if not bench_cell.has_blogpost():

                                # Get the Credentials for Requesting User
                                credential = get_credential_for_user(a_request_user)

                                # Get the Primary Blogging Engine
                                environment = get_primary_cpw_environment()

                                # Does the Credential have a Password
                                if credential.has_apppwd() and environment.is_wordpress_active():

                                    # Post a New Blogpost
                                    returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                                             bench_cell.title,
                                                                                             bench_cell.description)

                                    # Check the Post Response
                                    if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                        post_id = returned_blogpost['id']

                                    else:

                                        # If failure, Raise an Error!
                                        message = "WordPress Error - Contact System Administrator : " + \
                                            str(returned_blogpost) + '!'
                                        raise serializers.ValidationError(message)

                            # Set the Cell Blogpost to the new Blogpost
                            bench_cell.set_blogpost(post_id)

                        # If there is a Database Image and there is a Supplied Image
                        if image_data is not None and bench_cell.image is not None:

                            # Extract the supplied Image Attributes 
                            image_server = image_data.get('server')
                            owner = image_data.get('owner')
                            image_id = image_data.get('image_id')
                            image_roi_id = image_data.get('roi')
                            image_comment = image_data.get('comment')
                            image_hidden = False

                            # Get the User Object for the Supplied Image Owner
                            image_owner = get_user_from_username(owner)

                            image_identifier = int(image_id)

                            # Is the Suppied Image Id Different to the Existing Database Image Id?
                            #  Yes ...
                            if image_identifier == bench_cell.image.identifier:

                                # Validate the new supplied Image Attributes, and return the associated Server
                                server = self.validate_image_json(image_server,
                                                                  image_owner,
                                                                  image_id,
                                                                  image_roi_id,
                                                                  image_comment)

                                image_name = ''
                                image_viewer_url = ''
                                image_birdseye_url = ''
                                image_roi = 0

                                # Is the Server a WordPress Server?
                                if server.is_wordpress():

                                    # Get the Image from the WordPress Server for the supplied Id
                                    data = server.check_wordpress_image(image_owner, image_id)

                                    json_image = data['image']

                                    # Extract the Server Image Attributes
                                    image_name = json_image['name']
                                    image_viewer_url = json_image['viewer_url']
                                    image_birdseye_url = json_image['birdseye_url']

                                # Is the Server an OMERO Server?
                                else:

                                    # Get the Image from the OMERO Server for the supplied Id
                                    data = server.check_imaging_server_image(image_id)

                                    json_image = data['image']

                                    # Extract the Server Image Attributes
                                    image_name = json_image['name']
                                    image_viewer_url = json_image['viewer_url']
                                    image_birdseye_url = json_image['birdseye_url']

                                    # Is there an ROI Suppied too?
                                    if image_roi_id != 0:

                                        # Get the Image ROI from the OMERO Server for the Supplied Roi Id
                                        data = server.check_imaging_server_image_roi(image_id, image_roi_id)

                                        json_roi = data['roi']

                                        # Extract the ROI Id
                                        image_roi = int(json_roi['id'])

                                # Does the Image already exist in the Database?
                                #  Yes
                                if exists_image_for_id_server_owner_roi(image_id, server, image_owner, image_roi):

                                    # Get the Existing Image
                                    existing_image_list = get_images_for_id_server_owner_roi(image_id,
                                                                                             server,
                                                                                             image_owner,
                                                                                             image_roi)

                                    image = existing_image_list[0]

                                    # Do we have a new Image comment
                                    #  Yes
                                    if image.comment != image_comment:

                                        # Set the Image Comment
                                        image.comment = image_comment

                                        # Update the Database
                                        image.save()

                                    # Is the requesting user Hiding Images in their Collections?
                                    #  Yes ...
                                    if a_request_user.profile.is_hide_collection_image():

                                        #  Set the Image Hidden flags to true
                                        image.set_hidden(True)

                                        # Update the Database
                                        image.save()

                            #  No ...
                            else:
                                # Validate the new supplied Image Attributes, and return the associated Server
                                server = self.validate_image_json(image_server,
                                                                  image_owner,
                                                                  image_id,
                                                                  image_roi_id,
                                                                  image_comment)

                                image_name = ''
                                image_viewer_url = ''
                                image_birdseye_url = ''
                                image_roi = 0

                                # Is the Server a WordPress Server?
                                if server.is_wordpress():

                                    # Get the Image from the WordPress Server for the supplied Id
                                    data = server.check_wordpress_image(image_owner, image_id)

                                    json_image = data['image']

                                    # Extract the Server Image Attributes
                                    image_name = json_image['name']
                                    image_viewer_url = json_image['viewer_url']
                                    image_birdseye_url = json_image['birdseye_url']

                                # Is the Server an OMERO Server?
                                else:

                                    # Get the Image from the OMERO Server for the supplied Id
                                    data = server.check_imaging_server_image(image_id)

                                    json_image = data['image']

                                    # Extract the Server Image Attributes
                                    image_name = json_image['name']
                                    image_viewer_url = json_image['viewer_url']
                                    image_birdseye_url = json_image['birdseye_url']

                                    # Is there an ROI Suppied too?
                                    if image_roi_id != 0:

                                        # Get the Image ROI from the OMERO Server for the Supplied Roi Id
                                        data = server.check_imaging_server_image_roi(image_id, image_roi_id)

                                        json_roi = data['roi']

                                        # Extract the ROI Id
                                        image_roi = int(json_roi['id'])

                                # Does the Image already exist in the Database?
                                #  Yes
                                if exists_image_for_id_server_owner_roi(image_id, server, image_owner, image_roi):

                                    # Get the Existing Image
                                    existing_image_list = get_images_for_id_server_owner_roi(image_id,
                                                                                             server,
                                                                                             image_owner,
                                                                                             image_roi)

                                    image = existing_image_list[0]

                                    # Do we have a new Image comment
                                    #  Yes
                                    if image.comment != image_comment:

                                        # Set the Image Comment
                                        image.comment = image_comment

                                        # Update the Database
                                        image.save()

                                    # Is the requesting user Hiding Images in their Collections?
                                    #  Yes ...
                                    if a_request_user.profile.is_hide_collection_image():

                                        #  Set the Image Hidden flags to true
                                        image.set_hidden(True)

                                        # Update the Database
                                        image.save()

                                    # Associate the Cell with the Existing Image
                                    bench_cell.image = image

                                # No ... 
                                else:

                                    # Create a New Image Object
                                    image = Image.create(image_id,
                                                         image_name,
                                                         server,
                                                         image_viewer_url,
                                                         image_birdseye_url,
                                                         image_roi,
                                                         image_owner,
                                                         image_comment,
                                                         image_hidden)

                                    # Is the requesting user Hiding Images in their Collections?
                                    #  Yes ...
                                    if a_request_user.profile.is_hide_collection_image():

                                        #  Set the Image Hidden flags to true
                                        image.set_hidden(True)

                                    # Save the New Object to the Database
                                    image.save()

                                    # Associate the Cell with the New Image
                                    bench_cell.image = image

                                collection = None

                                # Does the Requesting User have a Active Collection?
                                if exists_active_collection_for_user(a_request_user):

                                    # Get the Active Collection
                                    collection = get_active_collection_for_user(a_request_user)

                                # No ...
                                else:

                                    # Set up Attributes for a New Collection            
                                    collection_title = "A Default REST Collection"
                                    collection_description = "A Collection created by a REST Request"
                                    collection_owner = a_request_user

                                    # Create a New Collection Object
                                    collection = Collection.create(collection_title,
                                                                   collection_description,
                                                                   collection_owner)
                                    # Write the New Collection Object to the Database
                                    collection.save()

                                    # Set the New Collection to Requesting Users Active Collection
                                    a_request_user.profile.set_active_collection(collection)
                                    # Update the Database with the updated User.
                                    a_request_user.save()

                                # If the Image is Not already in the Collection
                                if not exists_collection_for_image(collection, image):

                                    # Add the Image to the Collection
                                    Collection.assign_image(image, collection)

                                post_id = ''

                                # Does the Cell have a Blogpost
                                if bench_cell.has_blogpost():

                                    # Get the Credentials for Requesting User
                                    credential = get_credential_for_user(a_request_user)

                                    # Get the Primary Blogging Engine
                                    environment = get_primary_cpw_environment()

                                    # Does the Credential have a Password
                                    if credential.has_apppwd() and environment.is_wordpress_active():

                                        # Delete the Associated Blogpost
                                        response = environment.delete_a_post_from_wordpress(credential,
                                                                                            bench_cell.blogpost)

                                        # Check the Delete Response
                                        if response != WORDPRESS_SUCCESS:

                                            # If failure, Raise an Error!
                                            message = "WordPress Error - Contact System Administrator : " + \
                                                str(returned_blogpost) + '!'
                                            raise serializers.ValidationError(message)

                                        # Post a New Blogpost
                                        returned_blogpost = \
                                            environment.post_a_post_to_wordpress(credential,
                                                                                 bench_cell.title,
                                                                                 bench_cell.description)

                                        # Check the Post Response
                                        if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                            post_id = returned_blogpost['id']

                                        else:

                                            # If failure, Raise an Error!
                                            message = "WordPress Error - Contact System Administrator : " + \
                                                str(returned_blogpost) + '!'
                                            raise serializers.ValidationError(message)

                                # Set the Cell Blogpost to the new Blogpost
                                bench_cell.set_blogpost(post_id)

                        # If there is a Database Image and there is No Supplied Image
                        if image_data is None and bench_cell.image is not None:

                            # Set the Cell Image to None
                            bench_cell.image = None

                            # Does the Cell have a Blogpost
                            if bench_cell.has_blogpost():

                                # Get the Credentials for Requesting User
                                credential = get_credential_for_user(a_request_user)

                                # Get the Primary Blogging Engine
                                environment = get_primary_cpw_environment()

                                # Does the Credential have a Password
                                if credential.has_apppwd() and environment.is_wordpress_active():

                                    # Delete the Associated Blogpost
                                    response = environment.delete_a_post_from_wordpress(credential,
                                                                                        bench_cell.blogpost)

                                    # Check the Delete Response
                                    if response != WORDPRESS_SUCCESS:

                                        # If failure, Raise an Error!
                                        message = "WordPress Error - Contact System Administrator : " + \
                                            str(returned_blogpost) + '!'
                                        raise serializers.ValidationError(message)

                            # Set the Cell Blogpost to Empty
                            bench_cell.set_blogpost('')

                        # Add the Cell to the Update List 
                        update_cell_list.append(bench_cell)

        # Process the Update List
        for update_cell in update_cell_list:

            # Save the Updated Cell
            update_cell.save()

    def delete_missing_cells(self, an_instance, a_request_user, a_cells_data):
        """Delete the Missing Cells from the Bench

        Process the supplied Cells and Delete them from the Bench.

        Parameters:
            an_instance:        The Bench to which the Cells will be Deleted.
            a_request_user:     The Requesting User.
            a_cells_data:       The supplied array of Cells JSON.

        Returns:
            None

        Raises:
            ValidationError:
                WordPress Error

        """

        delete_cell_list = list()

        # Get the Existing Cells associated with this Bench
        bench_cells = (an_instance.bench_cells).all()
        # Convert the QuerySet to a List
        bench_cells = list(bench_cells)

        # Process the Existing Cells
        for bench_cell in bench_cells:

            # Get the Existing Cell Id
            bench_cell_id = bench_cell.id

            delete_flag = True

            # Process the Supplied Cells
            for cell_data in a_cells_data:

                # Get the Supplied Cell Id
                cell_id = cell_data.get('id', 0)

                # If the Supplied Cell Id is IN the Existing Cells
                #  Ignore the Supplied Cell
                if cell_id == bench_cell_id:

                    delete_flag = False

            # The Bench Cell is NOT in the list of Supplied Cell, so can be deleted
            if delete_flag is True:

                # Add the Bench cell to the List of Deletes
                delete_cell_list.append(bench_cell)

        # Process the Cells to be Deleted
        for delete_cell in delete_cell_list:

            # If the Cell has an Associated Blogpost
            if delete_cell.has_blogpost():

                # Get the Credential for the Requesting User
                credential = get_credential_for_user(a_request_user)

                # Get the Primary Blogging Engine
                environment = get_primary_cpw_environment()

                # If the Requesting User has a Password
                if credential.has_apppwd() and environment.is_wordpress_active():

                    # Delete the Associated Blogpost
                    response = environment.delete_a_post_from_wordpress(credential, delete_cell.blogpost)

                    # Check the Response
                    if response != WORDPRESS_SUCCESS:

                        # If the Blogpost Delete was unsuccessful, then Raise an Error!
                        message = "WordPress Error - Contact System Administrator!"
                        raise serializers.ValidationError(message)

            # Delete the Cell
            delete_cell.delete()

    def add_new_cells(self, an_instance, a_request_user, a_cells_data):
        """Add the New Cells to the Bench

        Process the supplied Cells and add them to the Bench.

        Parameters:
            an_instance:        The Bench to which the Cells will be added.
            a_request_user:     The Requesting User.
            a_cells_data:       The supplied array of Cells JSON.

        Returns:
            None

        Raises:
            ValidationError:
                WordPress Error

        """

        # For each Cell ...
        for cell_data in a_cells_data:

            # Extract the Cell Attributes
            cell_id = cell_data.get('id', 0)
            cell_title = cell_data.get('title')
            cell_description = cell_data.get('description')
            cell_xcoordinate = cell_data.get('xcoordinate')
            cell_ycoordinate = cell_data.get('ycoordinate')
            cell_blogpost = "0"

            cell_image = None

            # If the Cell Id is Zero then we have a NEW Cell to Add
            if cell_id == 0:

                # Extract the Image Data
                image_data = cell_data.pop('image')

                # Do we have any Inage Data?
                #  No
                if image_data is None:

                    cell_image = None

                #  Yes
                else:

                    # Extract the Image Attributes
                    server = image_data.get('server')
                    owner = image_data.get('owner')
                    image_id = image_data.get('image_id')
                    roi_id = image_data.get('roi')
                    image_comment = image_data.get('comment')
                    image_hidden = False

                    # Get the User Object from the database for the supplied owner
                    image_owner = get_user_from_username(owner)

                    # Validate the Attrubutes and Return the Server associated with them
                    server = self.validate_image_json(server, image_owner, image_id, roi_id, image_comment)

                    image_name = ''
                    image_viewer_url = ''
                    image_birdseye_url = ''
                    image_roi = 0

                    # Is the Server a WordPress Server?
                    #  Yes
                    if server.is_wordpress():

                        # Get the Image Data from the Server for the supplied Id
                        data = server.check_wordpress_image(image_owner, image_id)

                        json_image = data['image']

                        # Get the Image Attributes from the Image Data
                        image_name = json_image['name']
                        image_viewer_url = json_image['viewer_url']
                        image_birdseye_url = json_image['birdseye_url']

                    #  No, Server must be an OMERO server then
                    else:

                        # Get the Image Data from the Server for the supplied Id
                        data = server.check_imaging_server_image(image_id)

                        json_image = data['image']

                        # Get the Image Attributes from the Image Data
                        image_name = json_image['name']
                        image_viewer_url = json_image['viewer_url']
                        image_birdseye_url = json_image['birdseye_url']

                        # Is there an ROI supplied
                        if roi_id != 0:

                            # Check the supplied ROI exists for the supplied Image
                            data = server.check_imaging_server_image_roi(image_id, roi_id)

                            json_roi = data['roi']

                            image_roi = int(json_roi['id'])

                    # Does the Image already exist in the database for the supplied attributes and owner?
                    #  Yes
                    if exists_image_for_id_server_owner_roi(image_id, server, image_owner, image_roi):

                        # Get the existing image from the database
                        existing_image_list = get_images_for_id_server_owner_roi(image_id,
                                                                                 server,
                                                                                 image_owner,
                                                                                 image_roi)

                        existing_image = existing_image_list[0]

                        cell_image = existing_image

                        # Is the requesting user Hiding Images in their Collections?
                        #  Yes ...
                        if a_request_user.profile.is_hide_collection_image():

                            #  Set the Image Hidden flags to true
                            cell_image.set_hidden(True)

                            # Update the Database
                            cell_image.save()

                    #  No, a new Image must be added to the database.
                    else:

                        # Create a New Image Object
                        cell_image = Image.create(image_id,
                                                  image_name,
                                                  server,
                                                  image_viewer_url,
                                                  image_birdseye_url,
                                                  image_roi,
                                                  owner,
                                                  image_comment,
                                                  image_hidden)

                        # Is the requesting user Hiding Images in their Collections?
                        #  Yes ...
                        if a_request_user.profile.is_hide_collection_image():

                            #  Set the Image Hidden flags to true
                            cell_image.set_hidden(True)

                        # Write the new Image Object to the database
                        cell_image.save()

                    # The Image Object must be added to a Collection; it cannot exist on its own.
                    collection = None

                    # Does the Requesting  User have an Active Collection?
                    #  Yes
                    if exists_active_collection_for_user(a_request_user):

                        # Get the Active Collection
                        collection = get_active_collection_for_user(a_request_user)

                    # No active Collection - setup a Default Active Collection then
                    else:

                        # Set up new Collection Attributes
                        collection_title = "A Default REST Collection"
                        collection_description = "A Collection created by a REST Request"
                        collection_owner = a_request_user

                        # Create the new Collection Object
                        collection = Collection.create(collection_title, collection_description, collection_owner)
                        # Write the new Collection Object to the Database
                        collection.save()

                        # Set the Users Active Collection to the new Collection Object
                        a_request_user.profile.set_active_collection(collection)
                        # Update the User to the database
                        a_request_user.save()

                    # If the Image is NOT in the Collection already                            
                    if not exists_collection_for_image(collection, cell_image):

                        # Add the Image to the Collection
                        Collection.assign_image(cell_image, collection)

                    post_id = ''

                    # Get the Credentials for the Requesting User
                    credential = get_credential_for_user(a_request_user)

                    # Get the Primary WordPress Server - Blogging Engine
                    environment = get_primary_cpw_environment()

                    # Does the Requesting User have a Password?
                    #  Yes
                    if credential.has_apppwd() and environment.is_wordpress_active():

                        # Create a Blog Post for the New Cell
                        returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                                 cell_title,
                                                                                 cell_description)

                        # Was the Post a success?
                        #  Yes
                        if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                            # Store the Post id
                            post_id = returned_blogpost['id']

                        #  No
                        else:

                            # Raise an Error!
                            message = "WordPress Error - Contact System Administrator : " + \
                                str(returned_blogpost) + '!'
                            raise serializers.ValidationError(message)

                    # Add the Post Id to the Cell
                    cell_blogpost = post_id

                # Create a New Cell Object
                cell = Cell.create(an_instance,
                                   cell_title,
                                   cell_description,
                                   cell_xcoordinate,
                                   cell_ycoordinate,
                                   cell_blogpost,
                                   cell_image)

                # Write the New Cell to the database
                cell.save()

    def validate_matrix_json_fields(self, a_title, a_description, a_height, a_width):
        """Validate the supplied JSON fields for the Bench

        Title and Description field overflows are trapped by the Django REST framework

        Validate the supplied Title, Description, Height and Width fields of a Bench

        Parameters:
            a_title:        The Supplied Title of the Bench.
            a_description:  The Supplied Title of the Bench.
            a_height:       The specified Height of the Cells in the Bench.
            a_width:        The specified Widt of the Cells in the Bench.

        Returns:
            None

        Raises:
            ValidationError:
                CPW_REST:0160 - Bench Title Length is greater than 255 Characters
            ValidationError:
                CPW_REST:0150 - Bench Description Length is greater than 4095 Characters
            ValidationError:
                CPW_REST:0110 - Bench Cell Height is greater than 450 Pixels
            ValidationError:
                CPW_REST:0120 - Bench Cell Height is less than 75 Pixels
            ValidationError:
                CPW_REST:0130 - Bench Cell Width greater than 450 Pixels
            ValidationError:
                CPW_REST:0140 - Bench Cell Width is less than 75 Pixels

        """

        len_title = len(a_title)
        len_description = len(a_description)

        # Is the Title greater than 255 Characters? IF so, Raise an Error!
        if len_title > CONST_255:

            message = 'CPW_REST:0160 ERROR! Bench Title Length (' + str(len_title) + ') is greater than 255!'
            raise serializers.ValidationError(message)

        # Is the Description greater than 4095 Characters? IF so, Raise an Error!
        if len_description > CONST_4095:

            message = 'CPW_REST:0150 ERROR! Bench Description Length (' + str(len_title) + ') is greater than 4095!'
            raise serializers.ValidationError(message)

        # Is the Height greater than 450 Pixels? IF so, Raise an Error!
        if a_height > CONST_450:

            message = 'CPW_REST:0110 ERROR! Bench Cell Height (' + str(a_height) + ') is greater than 450!'
            raise serializers.ValidationError(message)

        # Is the Height less than 75 Pixels? IF so, Raise an Error!
        if a_height < CONST_75:

            message = 'CPW_REST:0120 ERROR! Bench Cell Height (' + str(a_height) + ') is less than 75!'
            raise serializers.ValidationError(message)

        # Is the Width greater than 450 Pixels? IF so, Raise an Error!
        if a_width > CONST_450:

            message = 'CPW_REST:0130 ERROR! Bench Cell Width (' + str(a_width) + ') is greater than 450!'
            raise serializers.ValidationError(message)

        # Is the Width less than 75 Pixels? IF so, Raise an Error!
        if a_width < CONST_75:

            message = 'CPW_REST:0140 ERROR! Bench Cell Width (' + str(a_width) + ') is less than 75!'
            raise serializers.ValidationError(message)

    def validate_cells(self, a_cells_data, a_request_user, a_mode_flag):
        """Validate the supplied JSON fields for an array of Cells

        The Array of Cells must be between 3x3 and 10000x10000 cells
        For an Array of AxB Cells, ALL combinations of A and B MUST be present, 
         With NO Gaps OR Duplicates
        Image Data must NOT be present in Row/Column Header/Footer Cells
        If Image Data is in a Cell, then this must be Valid too.
        Creation is possible for ANY User;
         Update is only possible for Owners

        Parameters:
            a_cells_data:       An Array of Cells.
            a_request_user:     The Requesting User.
            a_mode_flag:        TRUE for Create;
                                FALSE for UPDATE.

        Returns:
            None

        Raises:
            ValidationError:
                CPW_REST:0230 - NO Cells supplied with Bench
            ValidationError:
                CPW_REST:0300 - Too many Columns in Bench
            ValidationError:
                CPW_REST:0310 - Too many Rows in Bench
            ValidationError:
                CPW_REST:0280 - Too few Columns in Bench
            ValidationError:
                CPW_REST:0290 - Too few Rows in Bench
            ValidationError:
                CPW_REST:0190 - Duplicate Cell
            ValidationError:
                CPW_REST:0220 - Missing Cell
            ValidationError:
                CPW_REST:0010 - An Image is not Permitted in Column Header
            ValidationError:
                CPW_REST:0020 - An Image is not Permitted in : Column Footer
            ValidationError:
                CPW_REST:0030 - An Image is not Permitted in : Row Header
            ValidationError:
                CPW_REST:0040 - An Image is not Permitted in : Row Footer
            ValidationError:
                CPW_REST:0090 - Attempting to Add an Image to a Bench for a different Owner
            ValidationError:
                CPW_REST:0080 - Attempting to Add an Image to a Bench WITHOUT a Title or Description

        """

        maxX = 0
        maxY = 0

        # Have any Cells been supplied with this Bench, if Not, Raise an Error!
        if not a_cells_data:

            message = 'CPW_REST:0230 ERROR! NO Cells supplied with Bench!'
            raise serializers.ValidationError(message)

        # Process the supplied Cells ...
        for cell_data in a_cells_data:

            # Extract the Cells Attributes 
            title = cell_data.get('title')
            description = cell_data.get('description')

            # Validate the Cell Attributes 
            self.validate_cell_json_fields(title, description)

            # Extract the Cell Coordinates
            currX = int(cell_data.get('xcoordinate', 0))
            currY = int(cell_data.get('ycoordinate', 0))

            # Save the largest X Coordinate
            if currX > maxX:

                maxX = currX

            # Save the largest Y Coordinate
            if currY > maxY:

                maxY = currY

        max_column_index = maxX
        max_row_index = maxY

        maxX += 1
        maxY += 1

        environment = get_primary_cpw_environment()

        # Do we have more than 10,000 Columns?
        if maxX > environment.maximum_rest_columns:

            message = 'CPW_REST:0300 ERROR! Too many Columns in Bench (' + str(maxX) + '); No more than ' + str() + \
                ' Columns allowed!'
            raise serializers.ValidationError(message)

        # Do we have more than 10,000 Rows?
        if maxY > environment.maximum_rest_rows:

            message = 'CPW_REST:0310 ERROR! Too many Rows in Bench (' + str(maxY) + '); No more than ' + str() + \
                ' Rows allowed!'
            raise serializers.ValidationError(message)

        # Do we have less than 3 Columns?
        if maxX < environment.minimum_rest_columns:

            message = 'CPW_REST:0280 ERROR! Too few Columns in Bench (' + str(maxX) + '); At least ' + str() +\
                ' Columns required!'
            raise serializers.ValidationError(message)

        # Do we have less than 3 Rows?
        if maxY < environment.minimum_rest_rows:

            message = 'CPW_REST:0290 ERROR! Too few Rows in Bench (' + str(maxY) + '); At least ' + str() + \
                ' Rows required!'
            raise serializers.ValidationError(message)

        # Initialise a 2D array for all possible cells ...
        bench_cells = [[0 for cc in range(maxY)] for rc in range(maxX)]

        i = 0

        # Set all entries in the 2D Array to False
        while i < maxX:

            j = 0

            while j < maxY:

                bench_cells[i][j] = False
                j += 1

            i += 1

        cnt = 0

        # Process all the supplied Cells, to find Duplicate Cells ...
        for cell_data in a_cells_data:

            cnt += 1

            # Extract the X and Y Coordinates
            i = cell_data.get('xcoordinate', 0)
            j = cell_data.get('ycoordinate', 0)

            # If there are already is a Cell at this X and Y Coordinate in the 2D Array,
            #  we have a Duplicate Cell, so Raise an Error!
            if bench_cells[i][j] is True:

                message = 'CPW_REST:0190 ERROR! Duplicate Cell : Column Index = ' + str(i) + ', Row Index = ' + \
                    str(j) + '!'
                raise serializers.ValidationError(message)

            # To mark the presence of a Cell at this X and Y Coordinate, set this entry in the 2D Array to True
            bench_cells[i][j] = True

        i = 0

        cnt = 0

        # Check all the entries in the 2D Array, to find Missing Cells ...
        #  For each Column ....
        while i < maxX:

            j = 0

            # For each Row ... 
            while j < maxY:

                cnt += 1

                # If the entry in the 2D Array is False, then we have a missing cell, 
                #  so Raise an Error!
                if bench_cells[i][j] is False:

                    message = 'CPW_REST:0220 ERROR! Missing Cell : Column Index = ' + str(i) + ', Row Index = ' + \
                        str(j) + '!'
                    raise serializers.ValidationError(message)

                j += 1

            i += 1

        # Process all the Cells in the Cell Data
        for cell_data in a_cells_data:

            image_data = cell_data.get('image')

            # Get the Image Attributes from the Image Data
            xcoordinate = cell_data.get('xcoordinate', 0)
            ycoordinate = cell_data.get('ycoordinate', 0)
            cell_title = cell_data.get('title')
            cell_description = cell_data.get('description')

            # Do we have Image Data ...
            if image_data is not None:

                # Do we have Image Data in the Column Header, if so, Raise an Error!
                if xcoordinate == CONST_ZERO:

                    message = 'CPW_REST:0010 ERROR! An Image is not Permitted in : Column Index = ' + \
                        str(xcoordinate) + '!'
                    raise serializers.ValidationError(message)

                # Do we have Image Data in the Column Footer, if so, Raise an Error!
                if xcoordinate == max_column_index:

                    message = 'CPW_REST:0020 ERROR! An Image is not Permitted in : Column Index = ' + \
                        str(xcoordinate) + '!'
                    raise serializers.ValidationError(message)

                # Do we have Image Data in the Row Header, if so, Raise an Error!
                if ycoordinate == CONST_ZERO:

                    message = 'CPW_REST:0030 ERROR! An Image is not Permitted in : Row Index = ' + \
                        str(ycoordinate) + '!'
                    raise serializers.ValidationError(message)

                # Do we have Image Data in the Row Footer, if so, Raise an Error!
                if ycoordinate == max_row_index:

                    message = 'CPW_REST:0040 ERROR! An Image is not Permitted in : Row Index = ' + \
                        str(ycoordinate) + '!'
                    raise serializers.ValidationError(message)

                # There must be a Title and Description for a Cell containing an Image, else Raise an Error
                if cell_title == '' or cell_description == '':

                    message = 'CPW_REST:0080 ERROR! Attempting to Add an Image to a Bench WITHOUT a Title or " + \
                        "Description!'
                    raise serializers.ValidationError(message)

            # Is there any Image data in the Cell?
            if image_data is not None:

                server = image_data.get('server')
                owner = image_data.get('owner')
                image_id = image_data.get('image_id')
                roi_id = image_data.get('roi')
                image_comment = image_data.get('comment')

                image_owner = None

                # Does the Image Owner exist on the Database?
                #  Yes
                if exists_user_for_username(owner):

                    image_owner = get_user_from_username(owner)

                    # Is the Mode is TRUE for Create?
                    if a_mode_flag is True:

                        # Is the Requesting User is NOT the Image Owner?
                        if a_request_user != image_owner:

                            # And the User is NOT a Super-User, then Raise an Error!
                            if not a_request_user.is_superuser:

                                message = 'CPW_REST:0090 ERROR! Attempting to Add an Image to a Bench for a " + \
                                    "different Owner: ' + str(owner) + '!'
                                raise serializers.ValidationError(message)

                # No User exists, Raise an Error!
                else:
                    message = 'CPW_REST:XXXX ERROR! Image Owner: ' + str(image_owner) + ' Does NOT Exist!'
                    raise serializers.ValidationError(message)

                # Validate the Image in the Cell
                server = self.validate_image_json(server, image_owner, image_id, roi_id, image_comment)

    def validate_cell_json_fields(self, a_title, a_description):
        """Validate the supplied JSON fields for a Cell

        Title and Description field overflows are trapped by the Django REST framework,
         so these next 2 checks are redundant

        Parameters:
            title:          The Title of the Collection, Maximum 255 Characters.
            description:    The Description of the Collection, Maximum 4095 Characters.

        Returns:
            None

        Raises:
            ValidationError: 
                CPW_REST:0180 - Title Too Long.
            ValidationError:
                CPW_REST:0170 - Description Too Long

        """

        len_title = len(a_title)
        len_description = len(a_description)

        # Is the Title greater than 255 Characters?
        if len_title > CONST_255:

            message = 'CPW_REST:0180 ERROR! Cell Title Length (' + str(len_title) + ') is greater than 255!'
            raise serializers.ValidationError(message)

        # Is the Description greater than 4095 Characters?
        if len_description > CONST_4095:

            message = 'CPW_REST:0170 ERROR! Cell Description Length (' + str(len_title) + ') is greater than 4095!'
            raise serializers.ValidationError(message)

    def validate_image_json(self, a_server_str, a_user, a_image_id, a_roi_id, a_image_comment):
        """Validates the supplied Server, Owner, Image Id and ROI ID Fields

        Finds a Server Object from the the supplied server string, and 
        Validates the supplied Owner, Image Id and ROI ID Fields against the 
         Server Object.

        Parameters:
            server_str:     A string with a URL appended to a UID with an '@'.
            user:           A User object.
            image_id:       A string of valid JSON.
            roi_id:         A string of valid JSON.

        Returns:
            A Server Object or None

        Raises:
            ValidationError:
                CPW_REST:XXXX - Image Comment Title Length is greater than 4095!
            ValidationError:
                CPW_REST:0330 - Image NOT Present on the WordPress Server
            ValidationError:
                CPW_REST:0250 - ROI NOT Present on the Server
            ValidationError:
                CPW_REST:0210 - Image NOT Present on the OMERO Server
            ValidationError:
                CPW_REST:0350 - Server Type is WordPress or OMERO
            ValidationError:
                CPW_REST:0270 - Server is Unknown

        """

        server = None

        len_comment = len(a_image_comment)

        # Is the Comment greater than 4095 Characters? IF so, Raise an Error!
        if len_comment > CONST_4095:

            message = 'CPW_REST:XXXX ERROR! Image Comment Title Length (' + str(len_comment) + \
                ') is greater than 4095!'
            raise serializers.ValidationError(message)

        # Split the Server String into UID and URL?
        server_list = a_server_str.split("@")

        server_uid = str(server_list[0])
        server_url = str(server_list[1])

        # Is there a Server for the supplied UID and URL combination?
        if exists_server_for_uid_url(server_uid, server_url):

            # Get the Server Object
            server = get_servers_for_uid_url(server_uid, server_url)

            # Is the Server a WordPress server?
            if server.is_wordpress():

                # Does the Image exist on the WordPress Server?
                if not self.validate_wordpress_image_id(server, a_user, a_image_id):

                    # No, then Error
                    message = 'CPW_REST:0330 ERROR! Image NOT Present on : ' + a_server_str + '!'
                    raise serializers.ValidationError(message)

            # No ...
            else:

                # Is the Server an OMERO Server?
                if server.is_omero547():

                    # Does the Image exist on the OMERO Server?
                    if self.validate_imaging_image_id(server, a_image_id):

                        # Was an ROI supplied with the Image? 
                        if a_roi_id != 0:

                            # Does the ROI for the Image exist?
                            if not self.validate_roi_id(server, a_image_id, a_roi_id):

                                # No such ROI, Raise Error!
                                message = 'CPW_REST:0250 ERROR! ROI ID ' + str(a_roi_id) + ', for Image ID ' + \
                                    str(a_image_id) + ", NOT Present on : " + a_server_str + '!'
                                raise serializers.ValidationError(message)

                    # No Image, then Error
                    else:

                        message = 'CPW_REST:0210 ERROR! Image ID ' + str(a_image_id) + ', NOT Present on : ' + \
                            a_server_str + '!'
                        raise serializers.ValidationError(message)

                # Not an OMERO server, then Error
                else:

                    message = 'CPW_REST:0350 ERROR! Server Type Unknown : ' + a_server_str + '!'
                    raise serializers.ValidationError(message)

        # No Server, then Error
        else:

            message = 'CPW_REST:0270 ERROR! Server Unknown : ' + a_server_str + '!'
            raise serializers.ValidationError(message)

        return server

    def validate_wordpress_image_id(self, a_server, a_user, a_image_id):
        """For a WordPress Image, Check the supplied Image Exists

        Checks that an Image exists on a WordPress Server

        Parameters:
            a_server:       A Server Object.
            a_user:         A User Object.
            a_image_id:     The Id of the Image on the WordPress Server.

        Returns:
            A Boolean

        Raises:
            None

        """

        # Get the WordPress Image Data from the Server
        data = a_server.check_wordpress_image(a_user, a_image_id)

        json_image = data['image']
        image_name = json_image['name']

        # If the Image data is Empty then the Image does NOT exist
        if image_name == "":
            return False
        else:
            return True

    def validate_imaging_image_id(self, a_server, a_image_id):
        """For an OMERO Image, Check the supplied Image Exists

        Checks that an Image exists on an OMERO Server

        Parameters:
            a_server:       A Server Object.
            a_image_id:     The Id of the Image on the OMERO Server.

        Returns:
            A Boolean

        Raises:
            None

        """

        # Get the OMERO Image Data from the Server
        data = a_server.check_imaging_server_image(a_image_id)

        json_image = data['image']
        image_name = json_image['name']

        if image_name == "":
            return False
        else:
            return True

    def validate_roi_id(self, a_server, a_image_id, a_roi_id):
        """For an OMERO Image ROI, Check the supplied ROI Exists

        Checks that an ROI within an Image exists on an OMERO Server.

        Parameters:
            a_server:       A Server Object.
            a_image_id:     The Id of the Image on the OMERO Server.
            a_roi_id:       The Id of the ROI within the Image on the OMERO Server.

        Returns:
            A Boolean

        Raises:
            None

        """

        # Get the OMERO ROI Data from the Server
        data = a_server.check_imaging_server_image_roi(a_image_id, a_roi_id)

        json_roi = data['roi']
        roi_id = json_roi['id']

        # If the ROI data is Empty then the Image does NOT exist
        if roi_id == "":
            return False
        else:
            return True
