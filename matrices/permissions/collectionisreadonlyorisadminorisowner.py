#!/usr/bin/python3
###!
# \file         matrixisreadonlyorisadminorisowneroriseditor.py
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
# The Matrix Is Read Only Or (User) Is Admin Or Is Owner Or Is Editor Permission.
###
from rest_framework import permissions

from matrices.routines import get_collection_authority_for_collection_and_user_and_requester
from matrices.routines import credential_exists
from matrices.routines import credential_apppwd


class CollectionIsReadOnlyOrIsAdminOrIsOwner(permissions.BasePermission):

    """
    Custom Object Level permission to allow:
        1. Read Only Access to the Collection;
        2. Write Access to Owners of an object to edit the object;
        3. Write Access to SuperUsers to edit the object;
        5. Write Access only granted to Users that can connect to WordPress.
    """
    def has_object_permission(self, request, view, obj):

        return_flag = False

        authority = get_collection_authority_for_collection_and_user_and_requester(obj, request.user)

        # Read permissions are allowed to any request,
        # Write permissions are allowed if the user is a SuperUser.
        if request.method in permissions.SAFE_METHODS:

            # A Users Authority must either be Editor, Owner or Admin for Write permission.
            if authority.is_viewer() == True or authority.is_owner() == True or authority.is_admin() == True:

                return_flag = True

        else:

            if request.user.is_superuser == True:

                return_flag = True

            else:

                # Write permissions are allowed for the owner of the bench/image.
                if obj.owner == request.user:

                    # A Users must have a Credential record and a Password to write to WordPress.
                    if credential_exists(request.user) == True and credential_apppwd(request.user) != '':

                        return_flag = True

                else:

                    # A Users Authority must either be Editor, Owner or Admin for Write permission.
                    if authority.is_owner() == True or authority.is_admin() == True:

                        # A Users must have a Credential record and a Password to write to WordPress.
                        if credential_exists(request.user) == True and credential_apppwd(request.user) != '':

                            return_flag = True

        return return_flag


    """
    Custom permission to allow:
        1. Read Only Access to the Bench/Matrix;
        2. Write Access to SuperUsers to edit the object;
        3. Write Access only granted to Users that can connect to WordPress.
    """
    def has_permission(self, request, view):

        return_flag = False

        # Read permissions are allowed to any request,
        # Write permissions are allowed if the user is a SuperUser.
        if request.user.is_superuser == True:

            return_flag = True

        else:

            # A Users must have a Credential record and a Password to write to WordPress.
            if credential_exists(request.user) == True and credential_apppwd(request.user) != '':

                return_flag = True

        return return_flag
