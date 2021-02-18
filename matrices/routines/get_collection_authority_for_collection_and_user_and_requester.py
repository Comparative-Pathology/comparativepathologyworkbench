from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps
from django.db.models import Q 


"""
    Get the Collection Authorisation for a particular Collection and particular User
"""
def get_collection_authority_for_collection_and_user_and_requester(a_collection, a_user):

    CollectionAuthority = apps.get_model('matrices', 'CollectionAuthority')

    CollectionAuthorisation = apps.get_model('matrices', 'CollectionAuthorisation')

    collection_authority = CollectionAuthority.create("NONE", a_user)

    if a_user.is_superuser:

        collection_authority.set_as_admin()

    else:

        if a_user == a_matrix.owner:

            collection_authority.set_as_owner()

        else:
    
            if CollectionAuthorisation.objects.filter(Q(collection=a_collection) & Q(permitted=a_user)).exists():
        
                collection_authorisation = CollectionAuthorisation.objects.get(Q(collection=a_collection) & Q(permitted=a_user))
                
                if collection_authorisation.collection_authority.is_owner():

                    collection_authority.set_as_owner()

                if collection_authorisation.collection_authority.is_admin():

                    collection_authority.set_as_admin()

                if collection_authorisation.collection_authority.is_viewer():

                    collection_authority.set_as_viewer()

            else:

                collection_authority.set_as_none()

    return collection_authority

