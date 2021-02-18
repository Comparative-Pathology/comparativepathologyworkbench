from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps
from django.db.models import Q 


"""
    Get the Authorisation for a particular Bench and particular User
"""
def get_authority_for_bench_and_user_and_requester(a_matrix, a_user):

    Authority = apps.get_model('matrices', 'Authority')

    Authorisation = apps.get_model('matrices', 'Authorisation')

    authority = Authority.create("NONE", a_user)

    if a_user.is_superuser:
        
        authority.set_as_admin()

    else:

        if a_user == a_matrix.owner:
        
            authority.set_as_owner()

        else:
    
            if Authorisation.objects.filter(Q(matrix=a_matrix) & Q(permitted=a_user)).exists():
        
                authorisation = Authorisation.objects.get(Q(matrix=a_matrix) & Q(permitted=a_user))
                
                if authorisation.authority.is_owner():
        
                    authority.set_as_owner()

                if authorisation.authority.is_admin():
        
                    authority.set_as_admin()

                if authorisation.authority.is_viewer():
        
                    authority.set_as_viewer()

                if authorisation.authority.is_editor():
        
                    authority.set_as_editor()
            
            else:
        
                authority.set_as_none()

    return authority

