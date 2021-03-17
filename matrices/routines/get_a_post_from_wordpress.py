#!/usr/bin/python3
###!
# \file         get_a_post_from_wordpress.py
# \author       Mike Wicks
# \date         March 2021
# \version      $Id$
# \par
# (C) University of Edinburgh, Edinburgh, UK
# (C) Heriot-Watt University, Edinburgh, UK
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be
# useful but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free
# Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
# \brief
# Get a Blog Post from Wordpress
###
from __future__ import unicode_literals

import base64, hashlib

from os import urandom

from django.apps import apps

from requests.exceptions import HTTPError


CMD_BLOG_GET_POST = 'GetPost'


"""
    Get a Blog Post from Wordpress
"""
def get_a_post_from_wordpress(user_name, post_id):

    Credential = apps.get_model('matrices', 'Credential')

    credential = Credential.objects.get(username=user_name)

    Blog = apps.get_model('matrices', 'Blog')

    blogGetPost = Blog.objects.get(name=CMD_BLOG_GET_POST)

    get_post_url = blogGetPost.protocol.name + '://' + blogGetPost.url_blog + '/' + blogGetPost.application + '/' + blogGetPost.preamble + '/' + post_id

    try:
        response = requests.get(get_post_url)

        response.raise_for_status()

        post_id = str(json.loads(response.content)['id'])

    except HTTPError as http_err:

        post = {'id': '',
            'date': '',
            'time': '',
            'author': '',
            'title': '',
            'content': '',
            'url': '',
            'status': f'HTTP error occurred: {http_err}'
        }

        return post

    except Exception as err:

        post = {'id': '',
            'date': '',
            'time': '',
            'author': '',
            'title': '',
            'content': '',
            'url': '',
            'status': f'Other error occurred: {err}'
        }

        return post

    else:

        data = response.json()

        post_id = data['id']
        datetime = data['date']
        splitdatetime = datetime.split("T")

        date = splitdatetime[0]
        time = splitdatetime[1]

        author = data['author']
        title = data['title']
        content = data['content']
        guid = data['guid']
        title_rendered = title['rendered']
        content_rendered = content['rendered']
        guid_rendered = guid['rendered']

        credential = Credential.objects.get(wordpress=author)

        post = {'id': str(post_id),
            'date': date,
            'time': time,
            'author': credential.username,
            'title': title_rendered,
            'content': content_rendered[:-5][3:].rstrip(),
            'url': guid_rendered,
            'status': 'Success!'
            }

    return post
