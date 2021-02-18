from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps
from django.db.models import Count


"""
    Get All Collections for All Users
"""
def collection_list_all():

    Collection = apps.get_model('matrices', 'Collection')

    queryset = Collection.objects.all().order_by('id')
    
    collections = list()
    
    for collection in queryset:
    
        sum_collections = Collection.objects.annotate(image_count=Count("images")).filter(id=collection.id)
        
        collection_image_count = 0
        
        for sum_collection in sum_collections:
            collection_image_count = sum_collection.image_count
            
        out_collection = ({
            'collection_id': collection.id, 
            'collection_title': collection.title, 
            'collection_description': collection.description, 
            'collection_owner': collection.owner.username,
            'collection_active': collection.active,
            'authorisation_id': "0", 
            'authorisation_authority': "ADMIN",
            'authorisation_permitted': collection.owner.username
            })

        collections.append(out_collection)
    
    return collections

