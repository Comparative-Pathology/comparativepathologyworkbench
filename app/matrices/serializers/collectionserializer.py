#!/usr/bin/python3
#
# ##
# \file         collectionserializer.py
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
# ##
#
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from matrices.models import Collection
from matrices.models import Image

from matrices.serializers import ImageSerializer

from matrices.routines import exists_image_for_id_server_owner_roi
from matrices.routines import exists_image_in_cells
from matrices.routines import exists_user_for_username
from matrices.routines import exists_server_for_uid_url
from matrices.routines import get_collections_for_image
from matrices.routines import get_images_for_id_server_owner_roi
from matrices.routines import get_user_from_username
from matrices.routines import get_servers_for_uid_url

CONST_255 = 255
CONST_4095 = 4095


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    """A Serializer of Collections

    A Serializer of Collections in the Comparative Pathology Workbench REST Interface

    This Serializer provides Create, Read and Update functions for a Collection

    Parameters:
        id:                 The (internal) Id of the Collection.
        url(Read Only):     The (internal) URL of the Collection.
        owner:              The Owner (User Model) of the Collection.
        title:              The Title of the Collection, Maximum 255 Characters.
        description:        The Description of the Collection, Maximum 4095 Characters.
        images:             An Array of Images or Null.

    """

    title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    description = serializers.CharField(max_length=4095, required=False, allow_blank=True)
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Collection
        fields = ('url', 'id', 'title', 'description', 'owner', 'images')
        read_only_fields = ('url', )

    def create(self, validated_data):
        """Create Method.

        Creates a NEW Collection Object from a Json Representation of a Collection.

        Parameters:
            validated_data:     A string of valid JSON.

        Returns:
            An Collection Object

        Raises:
            ValidationError:
                CPW_REST:0060 - Attempting to Create an Image for a different Owner.
            ValidationError:
                CPW_REST:0390 - Attempting to Add a new Collection for a different Owner
            ValidationError:
                CPW_REST:0490 - the Image Owner Does NOT Exist!

        """

        request_user = None

        request = self.context.get("request")

        # Do we have a User of the Request?
        if request and hasattr(request, "user"):

            request_user = request.user

        # No, Get the Token from the Request then
        else:

            user_id = Token.objects.get(key=request.auth.key).user_id
            request_user = User.objects.get(id=user_id)

        collection_title = ""
        collection_description = ""

        # Is there a Title supplied?
        if validated_data.get('title', None) is None:

            collection_title = ""

        # Yes
        else:

            collection_title = validated_data.get('title')

        # Is there a Description supplied?
        if validated_data.get('description', None) is None:

            collection_description = ""

        # Yes
        else:

            collection_description = validated_data.get('description')

        owner = validated_data.get('owner')

        collection_owner = None

        # Does the Image Owner exist on the Database?
        #  Yes
        if exists_user_for_username(owner):

            # Get the Image Owner Object
            collection_owner = get_user_from_username(owner)

        # No User exists, Raise an Error!
        else:

            message = 'CPW_REST:0490 ERROR! Image Owner: ' + str(owner) + ' Does NOT Exist!'
            raise serializers.ValidationError(message)

        # Check the supplied Owner of the Collection against the Requesting User
        #  If Requesting User is NOT the Owner of the Collection
        if request_user != collection_owner:

            # AND the Requesting User is NOT a Super-User, then Raise an Error!
            if not request_user.is_superuser:

                message = 'CPW_REST:0390 ERROR! Attempting to Add a new Collection for a different Owner: ' + \
                    str(collection_owner) + '!'
                raise serializers.ValidationError(message)

        # Validate the Collection Fields
        self.validate_collection_json_fields(collection_title, collection_description)

        collection = None

        image_list = list()

        # Are there any Images supplied with the Collection?
        #  No, just Create the Collection
        if validated_data.get('images', None) is None:

            # Create the Collection
            collection = Collection.create(collection_title, collection_description, collection_owner)

        # Yes ...
        else:

            # Get the Images Data
            images_data = validated_data.pop('images')

            # We are Creating NOT Updating a Collection
            create_flag = True

            # Check that the Image Ownerships are OK
            self.validate_collection_images(images_data, request_user, create_flag)

            # Create the Collection
            collection = Collection.create(collection_title, collection_description, collection_owner)

            # For each Image in the Images Data Array
            for image_data in images_data:

                image_server = image_data.get('server')
                owner = image_data.get('owner')
                image_id = image_data.get('image_id')
                image_roi_id = image_data.get('roi')
                image_comment = image_data.get('comment')
                image_hidden = False

                image_owner = None

                # Does the Image Owner exist on the Database?
                #  Yes
                if exists_user_for_username(owner):

                    # Get the Image Owner Object
                    image_owner = get_user_from_username(owner)

                    # If the Requesting User is NOT the Image Owner
                    if request_user != image_owner:

                        # And the User is NOT a Super-User, then Raise an Error!
                        if not request_user.is_superuser:

                            message = 'CPW_REST:0430 ERROR! Attempting to Add an Image to a Collection for a ' + \
                                'different Owner: ' + str(image_owner) + '!'
                            raise serializers.ValidationError(message)

                # No User exists, Raise an Error!
                else:

                    message = 'CPW_REST:0500 ERROR! Image Owner: ' + str(owner) + ' Does NOT Exist!'
                    raise serializers.ValidationError(message)

                # Validate the supplied Image attributes against the supplied Server, and return the Server
                server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id, image_comment)

                image_name = ''
                image_viewer_url = ''
                image_birdseye_url = ''
                image_roi = image_roi_id

                # If the Server is WordPress ... ?
                if server.is_wordpress():

                    # Get the image data off the Server
                    data = server.check_wordpress_image(image_owner, image_id)

                    json_image = data['image']

                    image_name = json_image['name']
                    image_viewer_url = json_image['viewer_url']
                    image_birdseye_url = json_image['birdseye_url']

                # If the Server is OMERO ... ?
                else:

                    # Get the Image data off the Server
                    data = server.check_imaging_server_image(image_id)

                    json_image = data['image']

                    image_name = json_image['name']
                    image_viewer_url = json_image['viewer_url']
                    image_birdseye_url = json_image['birdseye_url']

                    # Do we have an ROI ... ?
                    if image_roi_id != 0:

                        # Get the ROW Image data off the Server
                        data = server.get_imaging_server_image_roi_json(image_id, image_roi_id)

                        json_roi = data['roi']
                        shape = json_roi['shape']

                        image_viewer_url = shape['viewer_url']
                        image_birdseye_url = shape['shape_url']

                # Does the image in the JSON already exist as an Image in the CPW?
                #  Yes - Get the existing Image and add that to the Image List for the Collection
                if exists_image_for_id_server_owner_roi(image_id, server, image_owner, image_roi):

                    existing_image_list = get_images_for_id_server_owner_roi(image_id, server, image_owner, image_roi)

                    image_in = existing_image_list[0]

                    image_list.append(image_in)

                #  No - Create a NEW Image and add that to the Image List for the Collection
                else:

                    image_in = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_roi, image_owner, image_comment, image_hidden)

                    # Update the Database with the New Image
                    image_in.save()

                    image_list.append(image_in)

        # Update the Database with the New Collection
        collection.save()

        # Does the User have an Active Image Collection?
        if not request_user.profile.has_active_collection():

            # Make the new Collection Object the User's Active Collection
            request_user.profile.set_active_collection(collection)
            request_user.save()

        # Add All the Images in Image List to the New Collection
        for image_out in image_list:

            Collection.assign_image(image_out, collection)

        # RETURN the created Collection Object
        return collection

    def update(self, instance, validated_data):
        """Update Method.

        Updates an EXISTING Collection Object from a Json Representation of a Collection.

        Parameters:
            instance:           an existing Collection Object
            validated_data:     A string of valid JSON.

        Returns:
            An Collection Object

        Raises:
            ValidationError:
                CPW_REST:0400 - Attempting to Update an existing Collection belonging to a different Owner
            ValidationError:
                CPW_REST:0510 - the Image Owner Does NOT Exist!

        """

        request_user = None

        request = self.context.get("request")

        # Do we have a User of the Request?
        if request and hasattr(request, "user"):

            request_user = request.user

        # No, Get the Token from the Request then
        else:

            user_id = Token.objects.get(key=request.auth.key).user_id
            request_user = User.objects.get(id=user_id)

        # Get the Collection Attributes from the JSON
        collection_title = validated_data.get('title', instance.title)
        collection_description = validated_data.get('description', instance.description)

        owner = validated_data.get('owner')

        collection_owner = None

        # Does the Image Owner exist on the Database?
        #  Yes
        if exists_user_for_username(owner):

            # Get the Image Owner Object
            collection_owner = get_user_from_username(owner)

        # No User exists, Raise an Error!
        else:

            message = 'CPW_REST:0510 ERROR! Image Owner: ' + str(owner) + ' Does NOT Exist!'
            raise serializers.ValidationError(message)

        # Update the Collection Object Attributes
        instance.title = collection_title
        instance.description = collection_description

        # Check the supplied Owner of the Collection against the Requesting User
        #  If Requesting User is NOT the Owner of the Collection
        if request_user != collection_owner:

            # AND the Requesting User is NOT a Super-User, then Raise an Error!
            if not request_user.is_superuser:

                message = 'CPW_REST:0400 ERROR! Attempting to Update an existing Collection for a ' + \
                    'different Owner: ' + str(collection_owner) + '!'
                raise serializers.ValidationError(message)

        # Validate the Collection Fields
        self.validate_collection_json_fields(collection_title, collection_description)

        images_data = []

        # Get the Image data 
        if validated_data.get('images', None) != None:

            images_data = validated_data.pop('images')

        # We are Updating NOT Creating a Collection
        create_flag = False

        # Check that the Image Ownerships are OK
        self.validate_collection_images(images_data, request_user, create_flag)

        # Delete from the Collection Object any Images that are NOT in the JSON
        self.delete_missing_images(instance, images_data)

        # Add to the Collection Object any NEW Images that are in the JSON
        self.add_new_images(instance, images_data)

        # Does the User have an Active Image Collection?
        if not request_user.profile.has_active_collection():

            # Make the new Collection Object the User's Active Collection
            request_user.profile.set_active_collection(instance)
            request_user.save()

        # Update the Database with the Existing Collection
        instance.save()

        # RETURN the updated Collection Object
        return instance

    def validate_collection_json_fields(self, a_title, a_description):
        """Validate the supplied JSON fields.

        Title and Description field overflows are trapped by the Django REST framework,
         so these next 2 checks are redundant

        Parameters:
            title:          The Title of the Collection, Maximum 255 Characters.
            description:    The Description of the Collection, Maximum 4095 Characters.

        Returns:
            None

        Raises:
            ValidationError: CPW_REST:0380 - NO data supplied
            ValidationError: CPW_REST:0410 - Title Too Long.
            ValidationError: CPW_REST:0420 - Description Too Long

        """

        # Check we have been supplied with BOTH a Title and Description
        if a_title == '' and a_description == '':

            message = 'CPW_REST:0380 ERROR! NO data supplied for Collection Creation!'
            raise serializers.ValidationError(message)

        len_title = len(a_title)
        len_description = len(a_description)

        # Is the Title greater than 255 Characters?
        if len_title > CONST_255:

            message = 'CPW_REST:0410 ERROR! Collection Title Length (' + str(len_title) + ') is greater than 255!'
            raise serializers.ValidationError(message)

        # Is the Description greater than 4095 Characters?
        if len_description > CONST_4095:

            message = 'CPW_REST:0420 ERROR! Collection Description Length (' + str(len_title) + ') is greater than 4095!'
            raise serializers.ValidationError(message)

    def delete_missing_images(self, instance, a_images_data):
        """Deletes Missing Images from the Collection

        Takes the list of Images from the supplied JSON file, and compares this 
         to the list of existing images in the Collection.
        Performs a Set Comparison to produce a list of missing Ids.
        Takes the list of missing Ids are deletes these images, if:
         There is now other Colleciton for this Image
         The image is not used on a Bench

        Parameters:
            a_images_data:  An Array of Images.
            instance:       The Collection being updated.

        Returns:

        Raises:

        """

        # A list of Images to be Deleted
        delete_image_list = list()

        # A list of JSON Ids
        image_id_input_list = list()

        # A list of Database Ids
        image_id_exist_list = list()

        # Get All the images in the Collection 
        images = (instance.images).all()
        images = list(images)

        # For Each of the Images in the JSON file, get the Ids
        for image_data in a_images_data:

            image_id = image_data.get('image_id', 0)

            #  Add to list of JSON Ids
            image_id_input_list.append(image_id)

        # For Each of the Images in the Collection, get the Ids
        for collection_image in images:

            collection_image_id = collection_image.identifier

            #  Add to list of Database Ids
            image_id_exist_list.append(collection_image_id)

        # Delete the list of JSON Ids from the List of Database Ids
        set_difference = set(image_id_exist_list) - set(image_id_input_list)

        # The list of possible Images to be Deleted
        delete_image_list = list(set_difference)

        # For Each Id in the list of possible Images to be Deleted
        for delete_image_id in delete_image_list:

            # Get the Images for this Collection
            images = instance.get_all_images()

            # For Each Image in the Collection
            for image in images:

                # Does the Id to be Delete match the Image Id in the Collection?
                if delete_image_id == image.identifier:

                    # Get the Collections for this Image
                    collection_list = get_collections_for_image(image)

                    delete_flag = True

                    # For each of these Collections ... 
                    for collection_other in collection_list:

                        # If the Collection is not THIS Collection, Do NOT Delete, 
                        #  As the image is in ANOTHER Collection!
                        if instance != collection_other:

                            delete_flag = False

                        # If we are allowed to Delete
                        if delete_flag is True:

                            # ... And the Image is NOT used in a Bench, then ...
                            if not exists_image_in_cells(image):

                                # Delete the Image!
                                image.delete()

                        # No - Image exists in ANOTHER Collection
                        else:

                            # Delete the LinkONLY between the Image and Collection
                            Collection.unassign_image(image, instance)

    def add_new_images(self, an_instance, a_images_data):
        """Adds New Images to the Collection

        Takes the list of Images from the supplied JSON file, and compares this 
         to the list of existing images in the Collection.
        Performs a Set Comparison to produce a list of new Ids.
        Takes the list of new Ids are dds these images, if:
         There is now other Colleciton for this Image
         The image is not used on a Bench

        Parameters:
            a_images_data:  An Array of Images.
            an_instance:    The Collection being updated.

        Returns:

        Raises:
            ValidationError:
                CPW_REST:0520 - the Image Owner Does NOT Exist!

        """

        # A list of Images to be Added
        add_image_list = list()

        # A list of JSON Ids
        image_id_input_list = list()

        # A list of Database Ids
        image_id_exist_list = list()

        # Get All the images in the Collection 
        images = (an_instance.images).all()
        images = list(images)

        # For Each of the Images in the JSON file, get the Ids
        for image_data in a_images_data:

            image_id = image_data.get('image_id', 0)

            #  Add to list of JSON Ids
            image_id_input_list.append(image_id)

        # For Each of the Images in the Collection, get the Ids
        for collection_image in images:

            collection_image_id = collection_image.identifier

            #  Add to list of Database Ids
            image_id_exist_list.append(collection_image_id)

        # Delete the list of Database Ids from the List of JSON Ids
        set_difference = set(image_id_input_list) - set(image_id_exist_list)

        # The list of possible Images to be Added
        add_image_list = list(set_difference)

        # For Each Id in the list of possible Images to be Added
        for add_image_id in add_image_list:

            # For Each Image in the supplied list of JSON Images
            for image_data in a_images_data:

                # Get the Image Id 
                image_id = image_data.get('image_id', 0)

                new_image = None

                # If the JSON Image Id Matches the Possible Add Image Id
                if image_id == add_image_id:

                    # Get the Image Attributes
                    server = image_data.get('server')
                    owner = image_data.get('owner')
                    image_id = image_data.get('image_id')
                    roi_id = image_data.get('roi')
                    image_comment = image_data.get('comment')
                    image_hidden = False

                    owner = image_data.get('owner')

                    image_owner = None

                    # Does the Image Owner exist on the Database?
                    #  Yes
                    if exists_user_for_username(owner):

                        # Get the Image Owner Object
                        image_owner = get_user_from_username(owner)

                    # No User exists, Raise an Error!
                    else:

                        message = 'CPW_REST:0520 ERROR! Image Owner: ' + str(owner) + ' Does NOT Exist!'
                        raise serializers.ValidationError(message)

                    # Validate the supplied Image attributes against the supplied Server, and return the Server
                    server = self.validate_image_json(server, image_owner, image_id, roi_id, image_comment)

                    image_name = ''
                    image_viewer_url = ''
                    image_birdseye_url = ''
                    image_roi = 0

                    # if the Server is a WordPress Server
                    if server.is_wordpress():

                        # Get the Image data from the Server
                        data = server.check_wordpress_image(owner, image_id)

                        json_image = data['image']

                        # Set the Image attributes
                        image_name = json_image['name']
                        image_viewer_url = json_image['viewer_url']
                        image_birdseye_url = json_image['birdseye_url']

                    # if the Server is an OMERO Server
                    else:

                        # Get the Image data from the Server
                        data = server.check_imaging_server_image(image_id)

                        json_image = data['image']

                        # Set the Image attributes
                        image_name = json_image['name']
                        image_viewer_url = json_image['viewer_url']
                        image_birdseye_url = json_image['birdseye_url']

                        # Has an ROI been suppleid too?
                        if roi_id != 0:

                            # Get the ROI Image data from the Server
                            data = server.check_imaging_server_image_roi(image_id, roi_id)

                            json_roi = data['roi']

                            # Set the ROI Image attribute
                            image_roi = int(json_roi['id'])

                    # Has the potential New Image already been created by this User?
                    if exists_image_for_id_server_owner_roi(image_id, server, owner, image_roi):

                        # Get the existing Image
                        existing_image_list = get_images_for_id_server_owner_roi(image_id, server, owner, image_roi)

                        existing_image = existing_image_list[0]

                        # Assign the existing Image to the New Colleciton
                        Collection.assign_image(existing_image, an_instance)

                    # No - Create a New Image Object
                    else:

                        # Create a New Image Object with the gathered atttributes
                        new_image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_roi, owner, image_comment, image_hidden)

                        # Update the Database with the New Image
                        new_image.save()

                        # Assign the New Image to the New Colleciton
                        Collection.assign_image(new_image, an_instance)

    def validate_collection_images(self, a_images_data, a_request_user, a_mode_flag):
        """Validates the supplied Images in the Collection

        Finds a Server Object from the the supplied server string, and 
        Validates the supplied Owner, Image Id and ROI ID Fields against the 
         Server Object.

        Parameters:
            a_images_data:      An Array of Images.
            a_request_user:     The Requesting User.
            a_mode_flag:        TRUE for Create;
                                FALSE for UPDATE.

        Returns:

        Raises:
            ValidationError:
                CPW_REST:0430 - Attempting to add an Image that belongs to somebody else!
            ValidationError:
                CPW_REST:0530 - the Image Owner Does NOT Exist!

        """

        # For each Image in the supplied Array of Images
        for image_data in a_images_data:

            # Retrieve the Image
            image = image_data.get('image')

            # If there is an Image
            if image is not None:

                # Get the Image Owner
                owner = image.get('owner')

                image_owner = None

                # Does the Image Owner exist on the Database?
                #  Yes
                if exists_user_for_username(owner):

                    # Get the Image Owner Object
                    image_owner = get_user_from_username(owner)

                    # If the Mode is TRUE for Create
                    if a_mode_flag is True:

                        # If the Requesting User is NOT the Image Owner
                        if a_request_user != image_owner:

                            # And the User is NOT a Super-User, then Raise an Error!
                            if not a_request_user.is_superuser:

                                message = 'CPW_REST:0430 ERROR! Attempting to Add an Image to a Collection ' +\
                                    'for a different Owner: ' + str(image_owner) + '!'
                                raise serializers.ValidationError(message)

                # No User exists, Raise an Error!
                else:

                    message = 'CPW_REST:0530 ERROR! Image Owner: ' + str(owner) + ' Does NOT Exist!'
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
                CPW_REST:0540 - Image Comment Title Length is greater than 4095!
            ValidationError:
                CPW_REST:0440 - Image NOT Present on the WordPress Server
            ValidationError:
                CPW_REST:0450 - ROI NOT Present on the Server
            ValidationError:
                CPW_REST:0460 - Image NOT Present on the OMERO Server
            ValidationError:
                CPW_REST:0470 - Server Type is WordPress or OMERO
            ValidationError:
                CPW_REST:0480 - Server is Unknown

        """

        server = None

        len_comment = len(a_image_comment)

        # Is the Comment greater than 255 Characters? IF so, Raise an Error!
        if len_comment > CONST_4095:

            message = 'CPW_REST:0540 ERROR! Image Comment Title Length (' + str(len_comment) + ') is greater than 4095!'
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

                    message = 'CPW_REST:0320 ERROR! Image NOT Present on : ' + a_server_str + '!'
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
                                message = 'CPW_REST:0240 ERROR! ROI ID ' + str(a_roi_id) + ', for Image ID ' + \
                                    str(a_image_id) + ", NOT Present on : " + a_server_str + '!'
                                raise serializers.ValidationError(message)

                    # Image does not exist on the Server, Raise Error!
                    else:

                        message = 'CPW_REST:0200 ERROR! Image ID ' + str(a_image_id) + ', NOT Present on : ' + \
                            a_server_str + '!'
                        raise serializers.ValidationError(message)

                # No - Server type unrecognised, Raise Error!
                else:

                    message = 'CPW_REST:0340 ERROR! Server Type Unknown : ' + a_server_str + '!'
                    raise serializers.ValidationError(message)

        # No Server exists, Raise Error!
        else:

            message = 'CPW_REST:0260 ERROR! Server Unknown : ' + a_server_str + '!'
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

        # If the Image data is Empty then the Image does NOT exist
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
