from rest_framework import permissions


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
