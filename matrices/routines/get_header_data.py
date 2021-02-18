from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.shortcuts import get_object_or_404

from django.apps import apps

from . import credential_exists
from . import bench_list_by_user
from . import bench_list_not_by_user
from . import collection_list_by_user
from . import collection_list_not_by_user
from . import authorisation_list_select_related_bench_by_user
from . import collection_authorisation_list_select_related_collection_by_user
from . import get_active_collection_images_for_user
from . import exists_active_collection_for_user

"""
    Get the Data to Populate Base.html (The Header Template)
"""
def get_header_data(a_user):

    image_list = list()
    server_list = list()
    matrix_list = list()
    my_matrix_list = list()
    collection_list = list()
    my_collection_list = list()

    credential_flag = ''

    if not a_user.is_anonymous:

        Server = apps.get_model('matrices', 'Server')
        server_list = Server.objects.all()
        
        if exists_active_collection_for_user(a_user):
        
            image_list = get_active_collection_images_for_user(a_user)        

        if credential_exists(a_user) == True:
        
            credential_flag = a_user.username
            
        if a_user.is_superuser:
        
            matrix_list = bench_list_not_by_user(a_user)
            my_matrix_list = bench_list_by_user(a_user)
        
            collection_list = collection_list_not_by_user(a_user)
            my_collection_list = collection_list_by_user(a_user)

            collection_list_1 = collection_list_not_by_user(a_user)
            collection_list_2 = collection_list_by_user(a_user)
        
            collection_list = collection_list_1 + collection_list_2
            my_collection_list = collection_list_by_user(a_user)

        else:
        
            matrix_list_1 = bench_list_by_user(a_user)
            matrix_list_2 = authorisation_list_select_related_bench_by_user(a_user)
            
            matrix_list = matrix_list_1 + matrix_list_2
            my_matrix_list = bench_list_by_user(a_user)

            collection_list_1 = collection_list_by_user(a_user)
            collection_list_2 = collection_authorisation_list_select_related_collection_by_user(a_user)
        
            collection_list = collection_list_1 + collection_list_2
            my_collection_list = collection_list_by_user(a_user)
    
    data = { 'credential_flag': credential_flag, 'collection_list': collection_list, 'my_collection_list': my_collection_list, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list }
        
    return data

