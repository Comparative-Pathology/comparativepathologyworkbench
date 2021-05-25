#!/usr/bin/python3
###!
# \file         get_a_post_comments_from_wordpress.py
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
# Post a Blog Post to Wordpress
###
from __future__ import unicode_literals

import json, urllib, requests, base64, hashlib

from os import urandom

from django.apps import apps

from requests.exceptions import HTTPError


CMD_BLOG_GET_POST_COMMENTS = 'GetPostComments'


"""
    Post a Blog Post to Wordpress
"""
def get_a_post_comments_from_wordpress(post_id):

    Credential = apps.get_model('matrices', 'Credential')

    Blog = apps.get_model('matrices', 'Blog')

    blogGetPostComments = Blog.objects.get(name=CMD_BLOG_GET_POST_COMMENTS)

    get_post_comments_url = blogGetPostComments.protocol.name + '://' + blogGetPostComments.url_blog + '/' + blogGetPostComments.application + '/' + blogGetPostComments.preamble + post_id

    comment_list = list()

    try:
        response = requests.get(get_post_comments_url)

        response.raise_for_status()

    except HTTPError as http_err:

        comment = {'id': '',
                'date': '',
                'time': '',
                'author': '',
                'author_name': '',
                'content': '',
                'url': '',
                'status': f'HTTP error occurred: {http_err}'
        }

        comment_list.append(comment)

        return comment_list

    except Exception as err:

        comment = {'id': '',
                'date': '',
                'time': '',
                'author': '',
                'author_name': '',
                'content': '',
                'url': '',
                'status': f'Other error occurred: {err}'
        }

        comment_list.append(comment)

        return comment_list

    else:

        data = response.json()

        for c in data:

            comment_id = c['id']

            datetime = c['date']
            splitdatetime = datetime.split("T")

            date = splitdatetime[0]
            time = splitdatetime[1]

            author = c['author']
            author_name = c['author_name']
            content = c['content']
            link = c['link']
            content_rendered = content['rendered']

            credential = Credential.objects.get(wordpress=str(author))

            comment = {'id': str(comment_id),
                'date': date,
                'time': time,
                'author': str(author),
                'author_name': credential.username,
                'content': content_rendered[:-5][3:].rstrip(),
                'url': link,
                'status': 'Success!'
            }

            comment_list.append(comment)

        comment_list.reverse()

    return comment_list
