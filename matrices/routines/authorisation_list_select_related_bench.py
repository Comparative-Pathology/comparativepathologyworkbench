from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps


"""
    Get All Bench Authorisations for All Benches
"""
def authorisation_list_select_related_bench():

    Authorisation = apps.get_model('matrices', 'Authorisation')

    queryset = Authorisation.objects.select_related('matrix').all()
    
    matrices = list()
    
    for authorisation in queryset:
    
        out_matrix = ({
            'matrix_id': authorisation.matrix.id, 
            'matrix_title': authorisation.matrix.title, 
            'matrix_description': authorisation.matrix.description, 
            'matrix_blogpost': authorisation.matrix.blogpost, 
            'matrix_created': authorisation.matrix.created, 
            'matrix_modified': authorisation.matrix.modified, 
            'matrix_height': authorisation.matrix.height, 
            'matrix_width': authorisation.matrix.width, 
            'matrix_owner': authorisation.matrix.owner.username,
            'authorisation_id': authorisation.id, 
            'authorisation_authority': authorisation.authority.name,
            'authorisation_permitted': authorisation.permitted.username})
               
        matrices.append(out_matrix)
    
    return matrices

