from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps

from . import get_primary_wordpress_server


"""
    Return the Credential for a particular User
"""
def get_blog_link_post_url():

    Blog = apps.get_model('matrices', 'Blog')
    
    blogLinkPost = Blog.objects.get(name='LinkPost')

    serverWordpress = get_primary_wordpress_server()

    link_post_url = blogLinkPost.protocol.name + '://' + serverWordpress.url_server + '/' + blogLinkPost.application + '/'

    return link_post_url
