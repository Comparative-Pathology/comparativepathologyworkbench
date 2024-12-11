#!/usr/bin/python3
#
# ##
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
# This Serializer provides Create, Read and Update functions for an Image
# ##
#
from django.contrib.auth.models import User

from rest_framework import serializers

from rest_framework.authtoken.models import Token

from matrices.models import Image
from matrices.models import Collection

from matrices.routines import exists_collection_for_image
from matrices.routines import exists_server_for_uid_url
from matrices.routines import exists_user_for_username
from matrices.routines import get_servers_for_uid_url
from matrices.routines import get_user_from_username

CONST_4095 = 4095


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    """A Serializer of Images

    A Serializer of Images in the Comparative Pathology Workbench REST Interface

    This Serializer provides Create, Read and Update functions for an Image

    Parameters:
        id(Read Only):      The (internal) Id of the Image.
        url(Read Only):     The (internal) URL of the Image.
        owner:              The Owner (User Model) of the Image.
        server:             The Title of the Server, Maximum 255 Characters.
        image_id:           The identifier of the Image as stored on the Server.
        roi:                The ROI within the Image as stored on the Server.

    """

    roi = serializers.IntegerField(default=0)
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    server = serializers.CharField()
    image_id = serializers.IntegerField(default=0)
    comment = serializers.CharField(max_length=4095, required=False, allow_blank=True)

    class Meta:
        model = Image
        fields = ('url', 'id', 'owner', 'roi', 'server', 'image_id', 'comment')
        read_only_fields = ('id', 'url' )

    def create(self, validated_data):
        """Create Method.

        Creates a NEW Image Object from a Json Representation of an Image.

        Parameters:
            validated_data:     A string of valid JSON.

        Returns:
            An Image Object

        Raises:
            ValidationError:
                CPW_REST:0060 - Attempting to Create an Image for a different Owner.
            ValidationError:
                CPW_REST:0530 - the Image Owner Does NOT Exist!

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

        image_server = validated_data.get('server')
        owner = validated_data.get('owner')
        image_id = validated_data.get('image_id')
        image_roi_id = validated_data.get('roi')
        image_comment = validated_data.get('comment')
        image_hidden = False

        image_owner = None

        # Does the Image Owner exist on the Database?
        #  Yes
        if exists_user_for_username(owner):

            # Get the Image Owner Object
            image_owner = get_user_from_username(owner)

        # No User exists, Raise an Error!
        else:

            message = 'CPW_REST:0530 ERROR! Image Owner: ' + str(owner) + ' Does NOT Exist!'
            raise serializers.ValidationError(message)

        # Check the User in the Request matches the Supplied Image Owner
        if request_user != image_owner:

            if not request_user.is_superuser:

                message = 'CPW_REST:0060 ERROR! Attempting to Add a new Image for a different Owner: ' + str(image_owner) + '!'
                raise serializers.ValidationError(message)

        # Validate the Image Id, ROI, Owner, and Server and return the associated Server Object
        server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id, image_comment)

        collection = None

        # Does the User have an Active Image Collection?
        if request_user.profile.has_active_collection():

            # Yes - get the User's Active Image Collection
            collection = request_user.profile.active_collection

        else:

            # No
            collection_title = "A Default REST Collection"
            collection_description = "A Collection created by a REST Request"
            collection_owner = request_user

            # CREATE an new Collection Object!
            collection = Collection.create(collection_title, collection_description, collection_owner)
            collection.save()

            # Make the new Collection Object the User's Active Collection
            request_user.profile.set_active_collection(collection)
            request_user.save()

        image_name = ''
        image_viewer_url = ''
        image_birdseye_url = ''
        image_roi = 0

        # Is the Server is a WordPress Server?
        if server.is_wordpress():

            # Get the Image Data from the Server
            data = server.check_wordpress_image(image_owner, image_id)

            json_image = data['image']

            image_name = json_image['name']
            image_viewer_url = json_image['viewer_url']
            image_birdseye_url = json_image['birdseye_url']

        # Is the Server is an OMERO Server?
        else:

            # Get the Image Data from the Server
            data = server.check_imaging_server_image(image_id)

            json_image = data['image']

            image_name = json_image['name']
            image_viewer_url = json_image['viewer_url']
            image_birdseye_url = json_image['birdseye_url']

            # Was an ROI supplied?
            if image_roi_id != 0:

                # Get the Image and ROI Data from th Server
                data = server.check_imaging_server_image_roi(image_id, image_roi_id)

                json_roi = data['roi']
                image_roi = int(json_roi['id'])

        # CREATE an new Image Object!
        image = Image.create(image_id, image_name, server, image_viewer_url, image_birdseye_url, image_roi, image_owner, image_comment, image_hidden)
        image.save()

        # Add the Image to the User's Active Image Collection
        Collection.assign_image(image, collection)

        # RETURN the created Image Object
        return image

    def update(self, instance, validated_data):
        """Update Method.

        Updates an EXISTING Image Object from a Json Representation of an Image.

        Parameters:
            validated_data:     A string of valid JSON.

        Returns:
            An Image Object

        Raises:
            ValidationError:
                CPW_REST:0540 - the Image Owner Does NOT Exist!
            ValidationError:
                CPW_REST:0060 - Attempting to Create an Image for a different Owner.

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

        image_server = validated_data.get('server')
        owner = validated_data.get('owner', instance.owner)
        image_id = validated_data.get('image_id', instance.image_id)
        image_roi_id = validated_data.get('roi', instance.roi)
        image_comment = validated_data.get('comment', instance.comment)
        image_hidden = False

        image_owner = None

        # Does the Image Owner exist on the Database?
        #  Yes
        if exists_user_for_username(owner):

            # Get the Image Owner Object
            image_owner = get_user_from_username(owner)

        # No User exists, Raise an Error!
        else:

            message = 'CPW_REST:0540 ERROR! Image Owner: ' + str(owner) + ' Does NOT Exist!'
            raise serializers.ValidationError(message)


        # Check the User in the Request matches the Supplied Image Owner
        if request_user != image_owner:

            if not request_user.is_superuser:

                message = 'CPW_REST:0060 ERROR! Attempting to Add a new Image for a different Owner: ' + str(image_owner) + '!'
                raise serializers.ValidationError(message)

        # Validate the Image parameters against the Server and return the Server Object
        server = self.validate_image_json(image_server, image_owner, image_id, image_roi_id, image_comment)

        collection = None

        # Does the User have an Active Image Collection?
        if request_user.profile.has_active_collection():

            # Yes - get the User's Active Image Collection
            collection = request_user.profile.active_collection

        else:

            # No
            collection_title = "A Default REST Collection"
            collection_description = "A Collection created by a REST Request"
            collection_owner = request_user

            # CREATE an new Collection Object!
            collection = Collection.create(collection_title, collection_description, collection_owner)
            collection.save()

            # Make the new Collection Object the User's Active Collection
            request_user.profile.set_active_collection(collection)
            request_user.save()

        image_name = ''
        image_viewer_url = ''
        image_birdseye_url = ''
        image_roi = 0

        # Is the Server is a WordPress Server?
        if server.is_wordpress():

            # Get the Image Data from the Server
            data = server.check_wordpress_image(image_owner.id, image_id)

            json_image = data['image']

            image_name = json_image['name']
            image_viewer_url = json_image['viewer_url']
            image_birdseye_url = json_image['birdseye_url']

        # Is the Server is an OMERO Server?
        else:

            # Get the Image Data from the Server
            data = server.check_imaging_server_image(image_id)

            json_image = data['image']

            image_name = json_image['name']
            image_viewer_url = json_image['viewer_url']
            image_birdseye_url = json_image['birdseye_url']

            # Was an ROI supplied?
            if image_roi_id != 0:

                # Get the Image and ROI Data from the Server
                data = server.check_imaging_server_image_roi(image_id, image_roi_id)

                json_roi = data['roi']
                image_roi = int(json_roi['id'])

        # Update the Existing Image Attributes
        instance.server = server
        instance.owner = image_owner
        instance.image_id = image_id
        instance.identifier = image_id
        instance.name = image_name
        instance.viewer_url = image_viewer_url
        instance.birdseye_url = image_birdseye_url
        instance.roi = image_roi
        instance.comment = image_comment
        instance.hidden = image_hidden

        # UPDATE the Image Object
        instance.save()

        # If the Image is Not already in the Collection
        if not exists_collection_for_image(collection, instance):

            # Add the Image to the Collection
            Collection.assign_image(instance, collection)

        return instance

    def validate_image_json(self, a_server_str, a_user, a_image_id, a_roi_id, a_comment):
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
                CPW_REST:0550 - Image Comment Title Length is greater than 4095!
            ValidationError:
                CPW_REST:0320 - Image NOT Present on the WordPress Server
            ValidationError:
                CPW_REST:0240 - ROI NOT Present on the Server
            ValidationError:
                CPW_REST:0200 - Image NOT Present on the OMERO Server
            ValidationError:
                CPW_REST:0340 - Server Type is WordPress or OMERO
            ValidationError:
                CPW_REST:0260 - Server is Unknown

        """

        server = None

        len_comment = len(a_comment)

        # Is the Comment greater than 255 Characters? IF so, Raise an Error!
        if len_comment > CONST_4095:

            message = 'CPW_REST:0550 ERROR! Image Comment Title Length (' + str(len_comment) + ') is greater than 4095!'
            raise serializers.ValidationError(message)

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

            # No
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
                                message = 'CPW_REST:0240 ERROR! ROI ID ' + str(a_roi_id) + ', for Image ID ' + str(a_image_id) + ", NOT Present on : " + a_server_str + '!'
                                raise serializers.ValidationError(message)

                    # Image does not exist on the Server, Raise Error!
                    else:

                        message = 'CPW_REST:0200 ERROR! Image ID ' + str(a_image_id) + ', NOT Present on : ' + a_server_str + '!'
                        raise serializers.ValidationError(message)

                # No - Server type unrecognised, Raise Error!
                else:

                    message = 'CPW_REST:0340 ERROR! Server Type Unknown : ' + a_server_str + '!'
                    raise serializers.ValidationError(message)

            return server

        # No Server exists, Raise Error!
        else:

            message = 'CPW_REST:0260 ERROR! Server Unknown : ' + a_server_str + '!'
            raise serializers.ValidationError(message)

    def validate_wordpress_image_id(self, a_server, a_user, a_image_id):
        """For a WordPress Image, Check the supplied Image Exists

        Checks that an Image exists on a WordPress Server

        Parameters:
            server:     A Server Object.
            user:       A User Object.
            image_id:   The Id of the Image on the WordPress Server.

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
            server:     A Server Object.
            user:       A User Object.
            image_id:   The Id of the Image on the OMERO Server.

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
            server:     A Server Object.
            user:       A User Object.
            image_id:   The Id of the Image on the OMERO Server.
            roi_id:     The Id of the ROI within the Image on the OMERO Server.

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
