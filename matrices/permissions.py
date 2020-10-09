from rest_framework import permissions

from matrices.models import get_authority_for_matrix_and_user_and_requester


class MatrixIsReadOnlyOrIsAdminOrIsOwnerOrIsEditor(permissions.BasePermission):
    """
    Custom permission to allow:
        1. Read Only Access to the Bench/Matrix;
        2. Write Access to Owners of an object to edit the object;
        3. Write Access to SuperUsers to edit the object;
        4. Write Access to Users that have been given Editorship to edit the object.
    """

    def has_object_permission(self, request, view, obj):

        return_flag = False
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return_flag = True

        # Write permissions are allowed for the owner of the bench/image.
        if obj.owner == request.user:
            return_flag = True

        # Write permissions are allowed if the user is a SuperUser.
        if request.user.is_superuser == True:
            return_flag = True

        authority = get_authority_for_matrix_and_user_and_requester(obj, request.user)
        
        #if authority.is_viewer == True or authority.is_none == True:
        #    return_flag = False
		
        if authority.is_editor == True or authority.is_owner == True or authority.is_admin == True:
            return_flag = True
            
        return return_flag


class ImageIsReadOnlyOrIsAdminOrIsOwner(permissions.BasePermission):
    """
    Custom permission to allow:
        1. Read Only Access to the Image;
        2. Write Access to Owners of the Image to edit the Image;
        3. Write Access to SuperUsers to edit the the Image;
    """

    def has_object_permission(self, request, view, obj):

        return_flag = False
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return_flag = True

        # Write permissions are allowed for the owner of the bench/image.
        if obj.owner == request.user:
            return_flag = True

        # Write permissions are allowed if the user is a SuperUser.
        if request.user.is_superuser == True:
            return_flag = True

        return return_flag
