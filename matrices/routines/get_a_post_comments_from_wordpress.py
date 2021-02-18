from __future__ import unicode_literals

import base64, hashlib

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


