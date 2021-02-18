from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps
from django.db.models import Count


"""
    Get All Collection Authorisations for All Collections
"""
def collection_authorisation_list_select_related_collection():

    Collection = apps.get_model('matrices', 'Collection')

    CollectionAuthorisation = apps.get_model('matrices', 'CollectionAuthorisation')

    queryset = CollectionAuthorisation.objects.select_related('collection').all()
    
    collection_authorisations = list()
    
    for collection_authorisation in queryset:
    
        sum_collections = Collection.objects.annotate(image_count=Count("images")).filter(id=collection.id)
        
        collection_image_count = 0
        
        for sum_collection in sum_collections:

            collection_image_count = sum_collection.image_count
            
        out_collection_authorisation = ({
            'collection_id': collection_authorisation.collection.id, 
            'collection_title': collection_authorisation.collection.title, 
            'collection_description': collection_authorisation.collection.description, 
            'collection_owner': collection_authorisation.collection.owner.username,
            'collection_active': collection_authorisation.collection.active,
            'collection_image_count': str(collection_image_count),
            'authorisation_id': collection_authorisation.id, 
            'authorisation_authority': collection_authorisation.authority.name,
            'authorisation_permitted': collection_authorisation.permitted.username
        })
               
        collection_authorisations.append(out_collection_authorisation)
    
    return collection_authorisations

