#!/usr/bin/python3
# \file         environment.py
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
# The Environment Model.
###
from __future__ import unicode_literals

import json
import requests
import base64

from django.db import models
from django.contrib.auth.models import User

from django.apps import apps

from requests.exceptions import HTTPError

from matrices.models.location import Location
from matrices.models import Protocol

ENVIRONMENT_CZI = 'CZI'
ENVIRONMENT_CANADA = 'CANADA'
ENVIRONMENT_COELIAC = 'COELIAC'
ENVIRONMENT_DEVELOPMENT = 'DEVELOPMENT'

CMD_BLOG_GET_POST = 'GetPost'
CMD_BLOG_GET_POST_COMMENTS = 'GetPostComments'
CMD_BLOG_POST_A_POST = 'PostAPost'
CMD_BLOG_POST_A_COMMENT = 'PostAComment'
CMD_BLOG_DELETE_POST = 'DeletePost'
CMD_BLOG_GET_LINK_POST = 'LinkPost'


"""
    The Environment Model
"""


class Environment(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    location = models.ForeignKey(Location, related_name='environments', default=0, on_delete=models.DO_NOTHING)
    protocol = models.ForeignKey(Protocol, related_name='environments', default=0, on_delete=models.DO_NOTHING)
    web_root = models.CharField(max_length=255, blank=False, default='')
    document_root = models.CharField(max_length=255, blank=False, default='')
    wordpress_web_root = models.CharField(max_length=255, blank=False, default='')
    from_email = models.CharField(max_length=255, blank=False, default='')
    date_format = models.CharField(max_length=255, blank=False, default='%A, %B %e, %Y')
    owner = models.ForeignKey(User, related_name='environments', on_delete=models.DO_NOTHING)

    minimum_cell_height = models.IntegerField(default=75, blank=False)
    maximum_cell_height = models.IntegerField(default=450, blank=False)
    minimum_cell_width = models.IntegerField(default=75, blank=False)
    maximum_cell_width = models.IntegerField(default=450, blank=False)

    maximum_initial_columns = models.IntegerField(default=10, blank=False)
    minimum_initial_columns = models.IntegerField(default=1, blank=False)
    maximum_initial_rows = models.IntegerField(default=10, blank=False)
    minimum_initial_rows = models.IntegerField(default=1, blank=False)

    maximum_rest_columns = models.IntegerField(default=1000, blank=False)
    minimum_rest_columns = models.IntegerField(default=3, blank=False)
    maximum_rest_rows = models.IntegerField(default=1000, blank=False)
    minimum_rest_rows = models.IntegerField(default=3, blank=False)

    maximum_bench_count = models.IntegerField(default=10, blank=False)
    maximum_collection_count = models.IntegerField(default=10, blank=False)

    @classmethod
    def create(cls, name, location, protocol, web_root, document_root, wordpress_web_root, from_email, date_format,
               owner, minimum_cell_height, maximum_cell_height, minimum_cell_width, maximum_cell_width,
               maximum_initial_columns, minimum_initial_columns, maximum_initial_rows, minimum_initial_rows,
               maximum_rest_columns,  minimum_rest_columns, maximum_rest_rows, minimum_rest_rows, maximum_bench_count,
               maximum_collection_count):
        return cls(name=name, location=location, protocol=protocol, web_root=web_root, document_root=document_root,
                   wordpress_web_root=wordpress_web_root, from_email=from_email, date_format=date_format, owner=owner,
                   minimum_cell_height=minimum_cell_height, maximum_cell_height=maximum_cell_height,
                   minimum_cell_width=minimum_cell_width, maximum_cell_width=maximum_cell_width,
                   maximum_initial_columns=maximum_initial_columns, minimum_initial_columns=minimum_initial_columns,
                   maximum_initial_rows=maximum_initial_rows, minimum_initial_rows=minimum_initial_rows,
                   maximum_rest_columns=maximum_rest_columns, minimum_rest_columns=minimum_rest_columns,
                   maximum_rest_rows=maximum_rest_rows, minimum_rest_rows=minimum_rest_rows,
                   maximum_bench_count=maximum_bench_count, maximum_collection_count=maximum_collection_count)

    def __str__(self):
        return f"{self.id}, {self.name}, {self.location.id}, {self.protocol.id}, {self.web_root}, \
                {self.document_root}, {self.wordpress_web_root}, {self.from_email}, {self.date_format}, \
                {self.owner.id}, {self.minimum_cell_height}, {self.maximum_cell_height}, \
                {self.minimum_cell_width}, {self.maximum_cell_width}, \
                {self.maximum_initial_columns}, {self.minimum_initial_columns}, \
                {self.maximum_initial_rows}, {self.minimum_initial_rows}, \
                {self.maximum_rest_columns}, {self.minimum_rest_columns}, \
                {self.maximum_rest_rows}, {self.minimum_rest_rows}, \
                {self.maximum_bench_count}, {self.maximum_collection_count}"

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.location.id}, {self.protocol.id}, {self.web_root}, \
                {self.document_root}, {self.wordpress_web_root}, {self.from_email}, {self.date_format}, \
                {self.owner.id}, {self.minimum_cell_height}, {self.maximum_cell_height}, \
                {self.minimum_cell_width}, {self.maximum_cell_width}, \
                {self.maximum_initial_columns}, {self.minimum_initial_columns}, \
                {self.maximum_initial_rows}, {self.minimum_initial_rows}, \
                {self.maximum_rest_columns}, {self.minimum_rest_columns}, \
                {self.maximum_rest_rows}, {self.minimum_rest_rows}, \
                {self.maximum_bench_count}, {self.maximum_collection_count}"

    def get_full_web_root(self):
        return self.protocol.name + '://' + self.web_root

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False

    def is_czi(self):
        if self.location.name == ENVIRONMENT_CZI:
            return True
        else:
            return False

    def is_canada(self):
        if self.location.name == ENVIRONMENT_CANADA:
            return True
        else:
            return False

    def is_coeliac(self):
        if self.location.name == ENVIRONMENT_COELIAC:
            return True
        else:
            return False

    def is_development(self):
        if self.location.name == ENVIRONMENT_DEVELOPMENT:
            return True
        else:
            return False

    def set_owner(self, a_user):
        self.owner = a_user

    def set_date_format(self, a_date_format):
        self.date_format = a_date_format

    """
        Get a Blog Post from Wordpress
    """
    def get_a_post_from_wordpress(self, post_id):

        Credential = apps.get_model('matrices', 'Credential')

        Blog = apps.get_model('matrices', 'Blog')

        blogGetPost = Blog.objects.get(name=CMD_BLOG_GET_POST)

        get_post_url = blogGetPost.protocol.name + '://' + self.wordpress_web_root + '/' + blogGetPost.application + \
            '/' + blogGetPost.preamble + '/' + post_id

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

            print("Exception err : " + str(err))

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

    """
        Post a Blog Post to Wordpress
    """
    def get_a_post_comments_from_wordpress(self, post_id):

        Credential = apps.get_model('matrices', 'Credential')
        Blog = apps.get_model('matrices', 'Blog')

        blogGetPostComments = Blog.objects.get(name=CMD_BLOG_GET_POST_COMMENTS)

        get_post_comments_url = blogGetPostComments.protocol.name + '://' + self.wordpress_web_root + '/' + \
            blogGetPostComments.application + '/' + blogGetPostComments.preamble + post_id

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

            print("Exception err : " + str(err))

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

    """
        Post a Blog Post to WORDPRESS
    """
    def post_a_post_to_wordpress(self, credential, title, content):

        Blog = apps.get_model('matrices', 'Blog')

        blogPostAPost = Blog.objects.get(name=CMD_BLOG_POST_A_POST)

        post_a_post_url = blogPostAPost.protocol.name + '://' + self.wordpress_web_root + '/' + \
            blogPostAPost.application + '/' + blogPostAPost.preamble

        token_str = credential.username + ':' + credential.apppwd
        encoded_token_str = token_str.encode('utf8')

        token = base64.standard_b64encode(encoded_token_str)
        headers = {'Authorization': 'Basic ' + token.decode('utf8')}

        post = {'title': title,
                'content': content,
                'status': 'publish',
                'author': credential.wordpress,
                'format': 'standard'
                }

        post_id = ''

        try:
            response = requests.post(post_a_post_url, headers=headers, json=post)

            response.raise_for_status()

            post_id = str(json.loads(response.content)['id'])

        except HTTPError as http_err:

            post = {'id': '',
                    'title': title,
                    'content': content,
                    'status': 'publish',
                    'author': credential.wordpress,
                    'format': 'standard',
                    'status': f'HTTP error occurred: {http_err}'
                    }

        except Exception as err:

            print("Exception err : " + str(err))

            post = {'id': '',
                    'title': title,
                    'content': content,
                    'status': 'publish',
                    'author': credential.wordpress,
                    'format': 'standard',
                    'status': f'Other error occurred: {err}'
                    }

        else:

            post = {'id': post_id,
                    'title': title,
                    'content': content,
                    'status': 'publish',
                    'author': credential.wordpress,
                    'format': 'standard',
                    'status': 'Success!'
                    }

        return post

    """
        Post a Comment to a Blog Post WORDPRESS
    """
    def post_a_comment_to_wordpress(self, credential, post_id, content):

        Blog = apps.get_model('matrices', 'Blog')

        blogPostAComment = Blog.objects.get(name=CMD_BLOG_POST_A_COMMENT)

        post_a_comment_url = blogPostAComment.protocol.name + '://' + self.wordpress_web_root + '/' + \
            blogPostAComment.application + '/' + blogPostAComment.preamble

        token_str = credential.username + ':' + credential.apppwd
        encoded_token_str = token_str.encode('utf8')

        token = base64.standard_b64encode(encoded_token_str)
        headers = {'Authorization': 'Basic ' + token.decode('utf8')}

        comment = {
            'post': post_id,
            'content': content,
            'author': credential.wordpress,
            'format': 'standard'
            }

        try:
            response = requests.post(post_a_comment_url, headers=headers, json=comment)

            response.raise_for_status()

        except HTTPError as http_err:

            response = f'HTTP error occurred: {http_err}'

            comment = {
                'post': post_id,
                'content': content,
                'author': credential.wordpress,
                'format': 'standard',
                'status': f'HTTP error occurred: {http_err}'
            }

        except Exception as err:

            print("Exception err : " + str(err))

            comment = {
                'post': post_id,
                'content': content,
                'author': credential.wordpress,
                'format': 'standard',
                'status': f'Other error occurred: {err}'
            }

        else:

            comment = {
                'post': post_id,
                'content': content,
                'author': credential.wordpress,
                'format': 'standard',
                'status': 'Success!'
            }

        return comment

    """
        Delete a Blog Post from WORDPRESS
    """
    def delete_a_post_from_wordpress(self, credential, post_id):

        Blog = apps.get_model('matrices', 'Blog')

        blogDeletePost = Blog.objects.get(name=CMD_BLOG_DELETE_POST)

        delete_post_url = blogDeletePost.protocol.name + '://' + self.wordpress_web_root + '/' + \
            blogDeletePost.application + '/' + blogDeletePost.preamble + '/' + post_id

        token_str = credential.username + ':' + credential.apppwd
        encoded_token_str = token_str.encode('utf8')

        token = base64.standard_b64encode(encoded_token_str)
        headers = {'Authorization': 'Basic ' + token.decode('utf8')}

        response = ''

        try:
            response = requests.delete(delete_post_url, headers=headers)

            response.raise_for_status()

            post_id = str(json.loads(response.content)['id'])

        except HTTPError as http_err:

            response = f'HTTP error occurred: {http_err}'

        except Exception as err:

            print("Exception err : " + str(err))

            response = f'Other error occurred: {err}'

        else:

            response = 'Success!'

        return response

    """
        Get the Blog Link Post URL
    """
    def get_a_link_url_to_post(self):

        Blog = apps.get_model('matrices', 'Blog')

        blogLinkPost = Blog.objects.get(name=CMD_BLOG_GET_LINK_POST)

        link_post_url = blogLinkPost.protocol.name + '://' + self.wordpress_web_root + '/' + \
            blogLinkPost.application + '/'

        return link_post_url
