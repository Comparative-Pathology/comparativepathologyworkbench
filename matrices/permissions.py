from rest_framework import permissions

from matrices.models import get_authority_for_matrix_and_user_and_requester
from matrices.models import credential_exists
from matrices.models import credential_apppwd


class MatrixIsReadOnlyOrIsAdminOrIsOwnerOrIsEditor(permissions.BasePermission):

    """
    Custom Object Level permission to allow:
        1. Read Only Access to the Bench/Matrix;
        2. Write Access to Owners of an object to edit the object;
        3. Write Access to SuperUsers to edit the object;
        4. Write Access to Users that have been given Editorship to edit the object;
        5. Write Access only granted to Users that can connect to WordPress.
    """
    def has_object_permission(self, request, view, obj):

        return_flag = False
        
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # Write permissions are allowed if the user is a SuperUser.
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser == True:
        
            return_flag = True
        
        else:
        
            # Write permissions are allowed for the owner of the bench/image.
            if obj.owner == request.user:

                
                # A Users must have a Credential record and a Password to write to WordPress.
                if credential_exists(request.user) == True and credential_apppwd(request.user) != '':

                    return_flag = True

            else:

                authority = get_authority_for_matrix_and_user_and_requester(obj, request.user)
                
                # A Users Authority must either be Editor, Owner or Admin for Write permission.
                if authority.is_editor() == True or authority.is_owner() == True or authority.is_admin() == True:
                
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
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser == True:
        
            return_flag = True
        
        else:
        
            # A Users must have a Credential record and a Password to write to WordPress.
            if credential_exists(request.user) == True and credential_apppwd(request.user) != '':

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

        # Write permissions are allowed for the owner of the image.
        if obj.owner == request.user:
            return_flag = True

        # Write permissions are allowed if the user is a SuperUser.
        if request.user.is_superuser == True:
            return_flag = True

        return return_flag