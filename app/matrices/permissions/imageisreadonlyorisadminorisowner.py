#!/usr/bin/python3
# 
# ##
# \file         imageisreadonlyorisadminorisowner.py
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
# The Image Is Read Only Or (User) Is Admin Or Is Owner Permission.
# ##
#
from rest_framework import permissions


class ImageIsReadOnlyOrIsAdminOrIsOwner(permissions.BasePermission):
    """A Permission Class for Images

    Custom permission to allow:
        1. Read Only Access to the Image;
        2. Write Access to Owners of the Image to edit the Image;
        3. Write Access to SuperUsers to edit the the Image;

    Parameters:
        None

    """

    def has_object_permission(self, request, view, obj):
        """Does the Request have the relevant Permission?

        Check whether the Request is allowed to access the Object

        Parameters:

        Returns:

        Raises:
          
        """

        return_flag = False

        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return_flag = True

        # Write permissions are allowed for the owner of the image.
        if obj.owner == request.user:
            return_flag = True

        # Write permissions are allowed if the user is a SuperUser.
        if request.user.is_superuser:
            return_flag = True


        if request.user.username == 'guest':

            return_flag = False


        return return_flag
