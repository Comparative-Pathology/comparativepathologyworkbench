from __future__ import unicode_literals

from django.db import models
from django.db.models import Q 

from django.contrib.auth.models import User

from django.db.models.signals import post_save

from django.dispatch import receiver

from django.utils.timezone import now

from django.conf import settings

import requests

from requests.exceptions import HTTPError

from decouple import config

import json, urllib, requests, base64, hashlib

from django.shortcuts import get_object_or_404

from random import randint


from matrices.routines import AESCipher


WORDPRESS_SUCCESS = 'Success!'

MINIMUM = 75
MAXIMUM = 450

# Create your models here.

class Matrix(models.Model):
    title = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=4095, default='')
    blogpost = models.CharField(max_length=50, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    height = models.IntegerField(default=75, blank=False)
    width = models.IntegerField(default=75, blank=False)
    owner = models.ForeignKey(User, related_name='matrices', on_delete=models.DO_NOTHING)

    @classmethod
    #def create(cls, title, description, blogpost, created, modified, height, width, owner):
    #    return cls(title=title, description=description, blogpost=blogpost, created=created, modified=modified, height=height, width=width, owner=owner)
    def create(cls, title, description, blogpost, height, width, owner):
        return cls(title=title, description=description, blogpost=blogpost, height=height, width=width, owner=owner)
    
    def __str__(self):
        return f"{self.id}, {self.title}, {self.description}, {self.blogpost}, {self.owner.id}"
        
    def __repr__(self):
        return f"{self.id}, {self.title}, {self.description}, {self.blogpost}, {self.created}, {self.modified}, {self.height}, {self.width}, {self.owner.id}"
        
    def is_too_wide(self):
        if self.width > 450:
            return True
        else:
            return False
            
    def is_too_high(self):
        if self.height > 450:
            return True
        else:
            return False
            
    def is_not_wide_enough(self):
        if self.width < 75:
            return True
        else:
            return False
            
    def is_not_high_enough(self):
        if self.height < 75:
            return True
        else:
            return False
            
    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user

    def set_blogpost(self, a_blogpost):
        self.blogpost = a_blogpost

    def has_no_blogpost(self):
        if self.blogpost == '' or self.blogpost == '0':
            return True
        else:
            return False
            
    def has_blogpost(self):
        if self.blogpost == '' or self.blogpost == '0':
            return False
        else:
            return True
            
    def set_minimum_width(self):
        self.width = MINIMUM

    def set_minimum_height(self):
        self.height = MINIMUM

    def set_maximum_width(self):
        self.width = MAXIMUM

    def set_maximum_height(self):
        self.height = MAXIMUM


    def get_matrix(self):

        columns = self.get_columns()
        rows = self.get_rows()
    
        columnCount = self.get_column_count()
        rowCount = self.get_row_count()
    
        cells = Cell.objects.filter(matrix=self.id)
        
        matrix_cells=[[0 for cc in range(columnCount)] for rc in range(rowCount)]

        for i, row in enumerate(rows):
    
            row_cells=cells.filter(ycoordinate=i)
        
            for j, column in enumerate(columns):
            
                matrix_cell = row_cells.filter(xcoordinate=j)[0]
            
                matrix_cells[i][j] = matrix_cell
            
        return matrix_cells


    def validate_matrix(self):

        columns = self.get_columns()
        rows = self.get_rows()
    
        columnCount = self.get_column_count()
        rowCount = self.get_row_count()
    
        cells = Cell.objects.filter(matrix=self.id)
        
        matrix_cells=[[0 for cc in range(columnCount)] for rc in range(rowCount)]

        for i, row in enumerate(rows):
    
            row_cells=cells.filter(ycoordinate=i)
        
            for j, column in enumerate(columns):
            
                matrix_cell = row_cells.filter(xcoordinate=j)[0]
            
                matrix_cells[i][j] = matrix_cell
            
        return matrix_cells


    def get_rows(self):

        return Cell.objects.filter(matrix=self.id).values('ycoordinate').distinct()


    def get_row(self, a_row):

        return Cell.objects.filter(matrix=self.id).filter(ycoordinate=a_row)


    def get_columns(self):
    
        return Cell.objects.filter(matrix=self.id).values('xcoordinate').distinct()


    def get_column(self, a_column):

        return Cell.objects.filter(matrix=self.id).filter(xcoordinate=a_column)


    def get_row_count(self):

        return Cell.objects.filter(matrix=self.id).values('ycoordinate').distinct().count()


    def get_column_count(self):

        return Cell.objects.filter(matrix=self.id).values('xcoordinate').distinct().count()

    def get_max_row(self):
    
    	row_count = self.get_row_count()
    	
    	row_count = row_count - 1
    	
    	return row_count

    def get_max_column(self):
    
    	column_count = self.get_column_count()
    	
    	column_count = column_count - 1

    	return column_count

    """
        Get Matrix Cell Comments
    """
    def get_matrix_cell_comments(self):
    
        cells = Cell.objects.filter(matrix=self.id)
    
        cell_comment_list = list()
            
        for cell in cells:
    
            comment_list = list()
            
            error_flag = False
    
            if cell.has_blogpost() == True:
            
                comment_list = get_a_post_comments_from_wordpress(cell.blogpost)
            
                for comment in comment_list:
            
                    if comment['status'] != WORDPRESS_SUCCESS:
                    
                        error_flag = True
                        
            else:
                
                comment_list = []
            
            if error_flag == True:
            
                comment_list = []
            
    
            viewer_url = ''
            birdseye_url = ''
            image_name = ''
            image_id = ''
            
            if cell.has_image() == True:
            
                viewer_url = cell.image.viewer_url
                birdseye_url = cell.image.birdseye_url
                image_name = cell.image.name
                image_id = cell.image.id
                
            cellComments = ({
                    'id': cell.id,
                    'matrix_id': cell.matrix.id, 
                    'matrix_title': cell.matrix.title, 
                    'title': cell.title, 
                    'description': cell.description, 
                    'xcoordinate': cell.xcoordinate, 
                    'ycoordinate': cell.ycoordinate, 
                    'blogpost': cell.blogpost,
                    'image_id': image_id,
                    'viewer_url': viewer_url,
                    'birdseye_url': birdseye_url,
                    'image_name': image_name,
                    'comment_list': comment_list
                    })
            
            cell_comment_list.append(cellComments)
        
        return cell_comment_list
    
    
    """
        Get Matrix Comments
    """
    def get_matrix_comments(self):
    
        comment_list = list()
        
        error_flag = False
            
        if self.has_blogpost() == True:
            
            comment_list = get_a_post_comments_from_wordpress(self.blogpost)
            
            for comment in comment_list:
            
                if comment['status'] != WORDPRESS_SUCCESS:
                    
                    error_flag = True
                        
        else:
                
            comment_list = []
                
        if error_flag == True:
            
            comment_list = []
            
        matrixComments = ({
            'id': self.id,
            'title': self.title, 
            'description': self.description, 
            'blogpost': self.blogpost,
            'comment_list': comment_list
        })
            
        return matrixComments
        
    

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    @classmethod
    def create(cls, user, bio, location, birth_date, email_confirmed):
        return cls(user=user, bio=bio, location=location, birth_date=birth_date, email_confirmed=email_confirmed)
    
    def __str__(self):
        return f"{self.id}, {self.bio}, {self.location}, {self.birth_date}, {self.email_confirmed}"
        
    def __repr__(self):
        return f"{self.id}, {self.user.id}, {self.bio}, {self.location}, {self.birth_date}, {self.email_confirmed}"


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Type(models.Model):
    name = models.CharField(max_length=12, blank=False, unique=True, default='')
    owner = models.ForeignKey(User, related_name='types', on_delete=models.DO_NOTHING)

    @classmethod
    def create(cls, name, owner):
        return cls(name=name, owner=owner)
    
    def __str__(self):
        return f"{self.name}"
        
    def __repr__(self):
        return f"{self.name}, {self.owner.id}"

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user
        

class Protocol(models.Model):
    name = models.CharField(max_length=12, blank=False, unique=True, default='')
    owner = models.ForeignKey(User, related_name='protocols', on_delete=models.DO_NOTHING)

    @classmethod
    def create(cls, name, owner):
        return cls(name=name, owner=owner)
    
    def __str__(self):
        return f"{self.name}"
        
    def __repr__(self):
        return f"{self.name}, {self.owner.id}"

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user
        

class Server(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    url_server = models.CharField(max_length=50, blank=False, default='')
    uid = models.CharField(max_length=50, blank=True, default='')
    pwd = models.CharField(max_length=50, blank=True, default='')
    type = models.ForeignKey(Type, related_name='servers', default=0, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='servers', on_delete=models.DO_NOTHING)
    
    @classmethod
    def create(cls, name, url_server, uid, pwd, type, owner):
        return cls(name=name, url_server=url_server, uid=uid, pwd=pwd, type=type, owner=owner)
    
    def __str__(self):
        #return f"{self.id}, {self.name}, {self.url_server}, {self.uid}, {self.pwd}, {self.type.id}, {self.owner.id}"
        return f"{self.uid}@{self.url_server}"
        
    def __repr__(self):
        return f"{self.id}, {self.name}, {self.url_server}, {self.uid}, {self.pwd}, {self.type.id}, {self.owner.id}"


    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user
        
    def set_pwd(self, a_pwd):
        self.pwd = a_pwd
        
    def is_wordpress(self):
        if  self.type.name == 'WORDPRESS':
            return True
        else:
            return False

    def is_omero547(self):
        if  self.type.name == 'OMERO_5.4.7':
            return True
        else:
            return False

    def is_omero56(self):
        if  self.type.name == 'OMERO_5.6':
            return True
        else:
            return False

    def get_uid_and_url(self):
        return f"{self.uid}@{self.url_server}"


    """
        WORDPRESS INTERFACE
    """
    """
        Get a Blog Post from Wordpress
    """
    def get_wordpress_post(self, post_id):
    
        blogGetPost = Blog.objects.get(name='GetPost')
    
        get_post_url = blogGetPost.protocol.name + '://' + self.url_server + '/' + blogGetPost.application + '/' + blogGetPost.preamble + '/' + post_id
    
        #print("get_post_url : ", get_post_url)
    
        try:
            response = requests.get(get_post_url)
    
            response.raise_for_status()
            
            post_id = str(json.loads(response.content)['id'])
            
        except HTTPError as http_err:
            
            #print(f'get_a_post_from_wordpress - HTTP error occurred: {http_err}')
            
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
    
            #print(f'get_a_post_from_wordpress - Other error occurred: {err}')
    
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
    
            #print('get_a_post_from_wordpress - Success!')
    
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
    def get_wordpress_post_comments(self, post_id):
    
        blogGetPostComments = Blog.objects.get(name='GetPostComments')
    
        get_post_comments_url = blogGetPostComments.protocol.name + '://' + self.url_server + '/' + blogGetPostComments.application + '/' + blogGetPostComments.preamble + post_id
        
        #print("get_post_comments_url : ", get_post_comments_url)
    
        comment_list = list()
    
        try:
            response = requests.get(get_post_comments_url)
    
            response.raise_for_status()
                    
        except HTTPError as http_err:
            
            #print(f'get_a_post_comments_from_wordpress - HTTP error occurred: {http_err}')
    
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
    
            #print(f'get_a_post_comments_from_wordpress - Other error occurred: {err}')
    
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
    
            #print('get_a_post_comments_from_wordpress - Success!')
    
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
    
    
    """
        Post a Blog Post to WORDPRESS
    """
    def post_wordpress_post(self, user_name, title, content):
    
        credential = Credential.objects.get(username=user_name)
    
        blogPostAPost = Blog.objects.get(name='PostAPost')
    
        post_a_post_url = blogPostAPost.protocol.name + '://' + self.url_server + '/' + blogPostAPost.application + '/' + blogPostAPost.preamble
    
        #print("post_a_post_url : ", post_a_post_url)
        
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
        
            #print(f'HTTP error occurred: {http_err}')
            
            post = {'id': '',
                'title': title,
                'content': content,
                'status': 'publish',
                'author': credential.wordpress,
                'format': 'standard',
                'status': f'HTTP error occurred: {http_err}'
            }
    
        except Exception as err:
    
            #print(f'Other error occurred: {err}')
    
            post = {'id': '',
                'title': title,
                'content': content,
                'status': 'publish',
                'author': credential.wordpress,
                'format': 'standard',
                'status': f'Other error occurred: {err}'
            }
    
        else:
    
            #print('Success!')
    
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
    def post_wordpress_comment(self, user_name, post_id, content):
    
        credential = Credential.objects.get(username=user_name)
    
        blogPostAComment = Blog.objects.get(name='PostAComment')
    
        post_a_comment_url = blogPostAComment.protocol.name + '://' + self.url_server + '/' + blogPostAComment.application + '/' + blogPostAComment.preamble
     
        #print("post_a_comment_url : ", post_a_comment_url)
        
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
    
            #print(f'HTTP error occurred: {http_err}')
            
            response = f'HTTP error occurred: {http_err}'
            
            comment = {
                'post': post_id,
                'content': content,
                'author': credential.wordpress,
                'format': 'standard',
                'status': f'HTTP error occurred: {http_err}'
            }
    
        except Exception as err:
    
            #print(f'Other error occurred: {err}')
            
            comment = {
                'post': post_id,
                'content': content,
                'author': credential.wordpress,
                'format': 'standard',
                'status': f'Other error occurred: {err}'
            }
    
        else:
    
            #print('Success!')
            
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
    def delete_wordpress_post(self, user_name, post_id):
    
        credential = Credential.objects.get(username=user_name)
    
        blogDeletePost = Blog.objects.get(name='DeletePost')
    
        delete_post_url = blogDeletePost.protocol.name + '://' + self.url_server + '/' + blogDeletePost.application + '/' + blogDeletePost.preamble + '/' + post_id
    
        #print("delete_post_url : ", delete_post_url)
        
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
    
            #print(f'HTTP error occurred: {http_err}')
    
            response = f'HTTP error occurred: {http_err}'
    
        except Exception as err:
    
            #print(f'Other error occurred: {err}')
    
            response = f'Other error occurred: {err}'
    
        else:
    
            #print('Success!')
    
            response = 'Success!'
    
        return response
    
    
    
    """
        Get the JSON Details for the Requested Server
    """
    def get_wordpress_json(self, request, page_id):
    
        current_user = request.user
    
        cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
        password = cipher.decrypt(self.pwd)
        
        user = get_object_or_404(User, pk=request.user.id)
        credential = Credential.objects.get(username=request.user.username)
    
        commandWordpressImages = Command.objects.filter(type=self.type).get(name='WordpressImages')
        
        images_url = commandWordpressImages.protocol.name + '://' + self.url_server + '/' + commandWordpressImages.application + '/' + commandWordpressImages.preamble + page_id + commandWordpressImages.postamble + str(credential.wordpress)
    
        #print("images_url : " +  images_url)
            
        token_str = credential.username + ':' + credential.apppwd
        encoded_token_str = token_str.encode('utf8')
        
        token = base64.standard_b64encode(encoded_token_str)
        headers = {'Authorization': 'Basic ' + token.decode('utf8')}
    
        data = {}
    
        try:
    
            response = requests.get(images_url, headers=headers, timeout=5)
        
            if response.status_code == requests.codes.ok:
            
                media_data = response.json()
                
                images_list = list()
        
                image_count = 0
    
                for media in media_data:
                
                    #print("media : " + str(media))
    
                    id = media['id']
                    title = media['title']
                    title_rendered = title['rendered']
                    image_viewer_url = media['source_url']
                    media_details = media['media_details']
                    sizes = media_details['sizes']
                    thumbnail = sizes['thumbnail']
                    image_thumbnail_url = thumbnail['source_url']
                    medium = sizes['medium']
                    image_birdseye_url = medium['source_url']
    
                    image = ({
                        'id': id, 
                        'name': title_rendered,
                        'viewer_url': image_viewer_url,
                        'birdseye_url': image_birdseye_url,
                        'thumbnail_url': image_thumbnail_url
                    })
                    
                    image_count = image_count + 1
            
                    images_list.append(image)
    
                group = ''
                project_list = []
    
                prev_page = '1'
                next_page = '1'
        
                page_count = int(page_id) * 35
                image_total = ( ( int(page_id) - 1 ) * 35 ) + image_count
    
                
                if image_count < 35:
                
                    next_page = '1'
                    
                if image_total % 35 == 0:
        
                    next_page = int(page_id) + 1
                
                else:
    
                    next_page = '1'
    
                if int(page_id) == 1:
                    
                    prev_page = page_id
                    
                else: 
        
                    prev_page = int(page_id) - 1
            
    
                dataset = ({
                    'id': '0',
                    'name': 'Your WordPress Media Library',
    #                'imageCount': page_count,
                    'imageCount': image_total,
                    'prev_page': prev_page,
                    'next_page': next_page
                })
    
                #print dataset
        
                matrix_list = list()
                my_matrix_list = list()

                if request.user.is_superuser == True:
        
                    matrix_list = matrix_list_not_by_user(request.user)
                    my_matrix_list = matrix_list_by_user(request.user)
        
                else:
        
                    matrix_list_1 = matrix_list_by_user(request.user)
                    matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
            
                    matrix_list = matrix_list_1 + matrix_list_2
                    my_matrix_list = matrix_list_by_user(request.user)
            
                image_list = Image.objects.filter(owner=request.user).filter(active=True)
                server_list = Server.objects.all()

    
                data = { 'server': self, 'group': group, 'projects': project_list, 'images': images_list, 'dataset': dataset, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list }
            
            else:
    
                group = ''
                project_list = []
                images_list = list()
    
                matrix_list = list()
                my_matrix_list = list()

                if request.user.is_superuser == True:
        
                    matrix_list = matrix_list_not_by_user(request.user)
                    my_matrix_list = matrix_list_by_user(request.user)
        
                else:
        
                    matrix_list_1 = matrix_list_by_user(request.user)
                    matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
            
                    matrix_list = matrix_list_1 + matrix_list_2
                    my_matrix_list = matrix_list_by_user(request.user)
            
                image_list = Image.objects.filter(owner=request.user).filter(active=True)
                server_list = Server.objects.all()


                image_count = 0
    
                next_page = int(page_id)
                prev_page = '1'
    
                dataset = ({
                    'id': '0',
                    'name': 'Your WordPress Media Library',
                    'imageCount': image_count,
                    'prev_page': prev_page,
                    'next_page': next_page
                })
    
                data = { 'server': self, 'group': group, 'projects': project_list, 'images': images_list, 'dataset': dataset, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list }
        
        except Exception as e:
    
            #print 'Exception!', e
    
            group = ''
            project_list = []
            images_list = list()
    
            matrix_list = list()
            my_matrix_list = list()

            if request.user.is_superuser == True:
        
                matrix_list = matrix_list_not_by_user(request.user)
                my_matrix_list = matrix_list_by_user(request.user)
        
            else:
        
                matrix_list_1 = matrix_list_by_user(request.user)
                matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
            
                matrix_list = matrix_list_1 + matrix_list_2
                my_matrix_list = matrix_list_by_user(request.user)
            
            image_list = Image.objects.filter(owner=request.user).filter(active=True)
            server_list = Server.objects.all()

    
            image_count = 0
    
            next_page = int(page_id)
            prev_page = '1'
            
            if int(next_page) == 1:
            
                prev_page = '1'
    
            dataset = ({
                    'id': '0',
                    'name': 'Your WordPress Media Library',
                    'imageCount': image_count,
                    'prev_page': prev_page,
                    'next_page': next_page
            })
    
            data = { 'server': self, 'group': group, 'projects': project_list, 'images': images_list, 'dataset': dataset, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list }
    
        return data
    
    
    
    """
        Get the JSON Details for the Requested Image
    """
    def get_wordpress_image_json(self, request, image_id):
        
        current_user = request.user
    
        userid = self.uid
    
        cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
        password = cipher.decrypt(self.pwd)
        
        user = get_object_or_404(User, pk=request.user.id)
        credential = Credential.objects.get(username=request.user.username)
    
        commandWordpressImage = Command.objects.filter(type=self.type).get(name='WordpressImage')
        
        image_url = commandWordpressImage.protocol.name + '://' + self.url_server + '/' + commandWordpressImage.application + '/' + commandWordpressImage.preamble + '/' + image_id
        
        #print("image_url : " + image_url)
        
        token_str = credential.username + ':' + credential.apppwd
        encoded_token_str = token_str.encode('utf8')
        
        token = base64.standard_b64encode(encoded_token_str)
        headers = {'Authorization': 'Basic ' + token.decode('utf8')}
    
        data = {}
    
        try:
    
            response = requests.get(image_url, headers=headers, timeout=50)
    
            if response.status_code == requests.codes.ok:
            
                media_data = response.json()
                
                caption = media_data['caption']
                caption_rendered = caption['rendered']
                
                title = media_data['title']
                title_rendered = title['rendered']
                
                description = media_data['alt_text']
    
                image_viewer_url = media_data['source_url']
                media_details = media_data['media_details']
                sizes = media_details['sizes']
                thumbnail = sizes['thumbnail']
                image_thumbnail_url = thumbnail['source_url']
                medium = sizes['medium']
                image_birdseye_url = medium['source_url']
    
                image = ({
                    'id': image_id,
                    'name': title_rendered,
                    'caption': caption_rendered[:-5][3:].rstrip(),
                    'description': description,
                    'viewer_url': image_viewer_url,
                    'birdseye_url': image_birdseye_url,
                    'thumbnail_url': image_thumbnail_url
                })
    
                #print image
                #print("image : " + str(image))
    
                group = ''
                project_list = []
                datasets = []
                projects = []
        
                matrix_list = list()
                my_matrix_list = list()

                if request.user.is_superuser == True:
        
                    matrix_list = matrix_list_not_by_user(request.user)
                    my_matrix_list = matrix_list_by_user(request.user)
        
                else:
        
                    matrix_list_1 = matrix_list_by_user(request.user)
                    matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
            
                    matrix_list = matrix_list_1 + matrix_list_2
                    my_matrix_list = matrix_list_by_user(request.user)
            
                image_list = Image.objects.filter(owner=request.user).filter(active=True)
                server_list = Server.objects.all()

        
                data = { 'server': self, 'group': group, 'projects': projects, 'datasets': datasets, 'image': image, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list }
    
            else:
    
                image = ({
                    'id': image_id,
                    'name': '',
                    'caption': '',
                    'description': '',
                    'viewer_url': '',
                    'birdseye_url': '',
                    'thumbnail_url': ''
                })
    
                #print("image : " + image)

                group = ''
                project_list = []
                datasets = []
                projects = []
        
                matrix_list = list()
                my_matrix_list = list()

                if request.user.is_superuser == True:
        
                    matrix_list = matrix_list_not_by_user(request.user)
                    my_matrix_list = matrix_list_by_user(request.user)
        
                else:
        
                    matrix_list_1 = matrix_list_by_user(request.user)
                    matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
            
                    matrix_list = matrix_list_1 + matrix_list_2
                    my_matrix_list = matrix_list_by_user(request.user)
            
                image_list = Image.objects.filter(owner=request.user).filter(active=True)
                server_list = Server.objects.all()

        
                data = { 'server': self, 'group': group, 'projects': projects, 'datasets': datasets, 'image': image, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list }
    
        except Exception as e:
    
            #print('Exception!', e)
    
            image = ({
                'id': image_id,
                'name': '',
                'caption': '',
                'description': '',
                'viewer_url': '',
                'birdseye_url': '',
                'thumbnail_url': ''
            })
    
            group = ''
            project_list = []
            datasets = []
            projects = []
        
            matrix_list = list()
            my_matrix_list = list()

            if request.user.is_superuser == True:
        
                matrix_list = matrix_list_not_by_user(request.user)
                my_matrix_list = matrix_list_by_user(request.user)
        
            else:
        
                matrix_list_1 = matrix_list_by_user(request.user)
                matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
            
                matrix_list = matrix_list_1 + matrix_list_2
                my_matrix_list = matrix_list_by_user(request.user)
            
            image_list = Image.objects.filter(owner=request.user).filter(active=True)
            server_list = Server.objects.all()

        
            data = { 'server': self, 'group': group, 'projects': projects, 'datasets': datasets, 'image': image, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list }
    
        return data
            

    """
        OMERO INTERFACE
    """
    """
        Get the JSON Details for the Requested Server
    """
    def get_ebi_server_json(self, request):
    
        current_user = request.user
    
        experiments_url = 'https://www.ebi.ac.uk/gxa/sc/json/experiments/'
        
        session = requests.Session()
        session.timeout = 10
    
        payload = {'limit': 99}
        data = session.get(experiments_url, params=payload).json()
        assert len(data['experiments']) < 1000
    
        experiment_list = list()
    
        for p in data['experiments']:
            experiment = ({
                'experimentType': p['experimentType'],
                'experimentAccession': p['experimentAccession'],
                'experimentDescription': p['experimentDescription'],
                'loadDate': p['loadDate'],
                'lastUpdate': p['lastUpdate'],
                'numberOfAssays': p['numberOfAssays'],
                'numberOfContrasts': '',
                'species': p['species'],
                'kingdom': p['kingdom']
            })
            
            experiment_list.append(experiment)
    
        matrix_list = Matrix.objects.filter(owner=current_user)
        image_list = Image.objects.filter(owner=current_user).filter(active=True)
        server_list = Server.objects.all
    
        data = { 'server': self, 'experiment_list': experiment_list, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }
    
        return data
    
    
    """
        Get the JSON Details for the Requested Server
    """
    def get_ebi_widget_json(self, request):
    
        current_user = request.user
    
        matrix_list = Matrix.objects.filter(owner=current_user)
        image_list = Image.objects.filter(owner=current_user).filter(active=True)
        server_list = Server.objects.all
    
        data = { 'server': self, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }
    
        return data
    
    
    """
        Get the JSON Details for the Requested Server
    """
    def get_imaging_server_json(self, request):
    
        #print('STATICFILES_DIRS : ', settings.STATICFILES_DIRS)
        #print('BASE_DIR         : ', settings.BASE_DIR)
        #print('PROJECT_DIR      : ', settings.PROJECT_DIR)
        #print('STATIC_ROOT      : ', settings.STATIC_ROOT)
        #print('STATIC_URL       : ', settings.STATIC_URL)

        current_user = request.user
    
        commandAPI = Command.objects.filter(type=self.type).get(name='API')
        commandToken = Command.objects.filter(type=self.type).get(name='Token')
        commandLogin = Command.objects.filter(type=self.type).get(name='Login')
        commandProjects = Command.objects.filter(type=self.type).get(name='Projects')
        commandGroupProjects = Command.objects.filter(type=self.type).get(name='GroupProjects')
        commandGroupDatasets = Command.objects.filter(type=self.type).get(name='GroupDatasets')
        commandGroupImages = Command.objects.filter(type=self.type).get(name='GroupImages')
        commandDatasetImages = Command.objects.filter(type=self.type).get(name='DatasetImages')
        
        commandBirdsEye = Command.objects.filter(type=self.type).get(name='BirdsEye')
    
        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'
        
        projects_url = commandProjects.protocol.name + '://' + self.url_server + '/' + commandProjects.application + '/' + commandProjects.preamble
        group_projects_url = commandGroupProjects.protocol.name + '://' + self.url_server + '/' + commandGroupProjects.application + '/' + commandGroupProjects.preamble
        datasets_url = commandGroupDatasets.protocol.name + '://' + self.url_server + '/' + commandGroupDatasets.application + '/' + commandGroupDatasets.preamble
        images_url = commandGroupImages.protocol.name + '://' + self.url_server + '/' + commandGroupImages.application + '/' + commandGroupImages.preamble
        dataset_images_url = commandDatasetImages.protocol.name + '://' + self.url_server + '/' + commandDatasetImages.application + '/' + commandDatasetImages.preamble
        
        #print "api_url", api_url
        #print "token_url", token_url
        #print "login_url", login_url
        
        #proxies = {'http' : 'http://a.b.c.d:8080','https': 'https://a.b.c.d:4444'}
               
        session = requests.Session()
        session.timeout = 10
        #session.proxies = proxies
        
        try:
            r = session.get(api_url)
    
        except Exception as e:
    
            #print 'Exception!', e
                    
            matrix_list = Matrix.objects.filter(owner=current_user)
            image_list = Image.objects.filter(owner=current_user).filter(active=True)
            server_list = Server.objects.all
    
            group_count = 0
            group_list = []
        
            data = { 'server': self, 'group_list': group_list, 'group_count': group_count, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }
    
            return data    
    
        token = session.get(token_url).json()['data']
        session.headers.update({'X-CSRFToken': token, 'Referer': login_url})
        
        userid = self.uid
        
        cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
        password = cipher.decrypt(self.pwd)
    
        #print userid
        #print password
    
        memberOfGroup_list = list()
        
        group_list = list()
        
        group_count = 0
        
        if userid == "":
    
            project_url = projects_url + '/' + commandProjects.postamble
            #print project_url
    
            payload = {'limit': 50}
            project_rsp = session.get(project_url, params=payload)
            project_data = project_rsp.json()
            
            #print 'project_rsp.status_code', project_rsp.status_code
    
            if project_rsp.status_code == 200:
    
                project_meta = project_data['meta']
                projectCount = project_meta['totalCount']
    
                for p in project_data['data']:
    
                    details = p['omero:details']
    
                    groupdetails = details['group']
    
                    groupId = groupdetails['@id']
                    
                    group_list.append(groupId)
                
                prevgroup = ''
    
                new_group_list = list()
    
                for group in group_list:
    
                    if prevgroup != group:
    
                        new_group_list.append(group)
        
                    prevgroup = group
                
                memberOfGroup_list = new_group_list
        
    
        group_list = list()
        
    
        if userid != "":
        
            payload = {'username': userid, 'password': password, 'server': 1}
        
            r = session.post(login_url, data=payload)
            login_rsp = r.json()
            try:
                assert r.status_code == 200
                assert login_rsp['success']
        
            except AssertionError:
        
                matrix_list = Matrix.objects.filter(owner=current_user)
                image_list = Image.objects.filter(owner=current_user).filter(active=True)
                server_list = Server.objects.all
    
                group_count = 0
                group_list = []
        
                data = { 'server': self, 'group_list': group_list, 'group_count': group_count, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }
    
                return data
        
        
            eventContext = login_rsp['eventContext']
            memberOfGroups = eventContext['memberOfGroups']
            
            memberOfGroup_list = memberOfGroups
        
        for mog in memberOfGroup_list:
    
            group_project_url = group_projects_url + str(mog)
            image_url = images_url + str(mog) + commandGroupImages.postamble            
            dataset_url = datasets_url + str(mog) + commandGroupDatasets.postamble
    
            #print group_project_url
            #print image_url
            #print dataset_url
        
            payload = {'limit': 50}
            group_project_rsp = session.get(group_project_url, params=payload)
            group_project_data = group_project_rsp.json()
            
            #print 'group_project_rsp.status_code', group_project_rsp.status_code
    
            if group_project_rsp.status_code == 200:
    
                group_group_project_meta = group_project_data['meta']
                projectCount = group_group_project_meta['totalCount']
    
                groupName = ''
            
                groupImageCount = 0
                
                for p in group_project_data['data']:
    
                    details = p['omero:details']
    
                    groupdetails = details['group']
                    groupName = groupdetails['Name']
                    groupId = groupdetails['@id']
    
                    payload = {'limit': 100}
                    dataset_rsp = session.get(dataset_url, params=payload)
                    dataset_data = dataset_rsp.json()
            
                    #print 'dataset_rsp.status_code', dataset_rsp.status_code
                
                    datasetCount = ''
                
                    randImageID = ''
                    randImageName = ''
                    randomImageBEURL = ''
                            
                    if dataset_rsp.status_code == 200:
    
                        imageCount = 0
                            
                        dataset_meta = dataset_data['meta']
                        datasetCount = dataset_meta['totalCount']            
            
                        #print 'datasetCount', datasetCount
                        
                        if userid == "":
                        
                            randImageID = '999999'
                            randImageName = 'NONE'
                            randomImageBEURL = 'NONE'
                            
                        else:
                            
                            for d in dataset_data['data']:
                            
                                datasetId = d['@id']
                                
                                dataset_image_url = dataset_images_url + '/' + str(datasetId) + '/' + commandDatasetImages.postamble
    
                                #print 'dataset_image_url', dataset_image_url
    
                                payload = {'limit': 100}
                                dataset_image_rsp = session.get(dataset_image_url, params=payload)
                                dataset_image_data = dataset_image_rsp.json()
            
                                #print 'dataset_image_rsp.status_code', dataset_image_rsp.status_code
                                    
                                if dataset_image_rsp.status_code == 200:
    
                                    dataset_image_meta = dataset_image_data['meta']
                                    imageCount = dataset_image_meta['totalCount']
                                        
                                    groupImageCount = groupImageCount + imageCount
                                    
                                    #print 'imageCount', imageCount
                                    
                                    if imageCount > 0:
                                    
                                        randImageIndex = randint(0, (imageCount - 1))
                                        #randImageIndex = 0
                                        #print 'Random Image Index: ', randImageIndex
                
                                        count = 0
                    
                                        for i in dataset_image_data['data']:
                    
                                            if count == randImageIndex:
                                                randImageID = i['@id']
                                                randImageName = i['Name']
                                                break
                            
                                            count = count + 1
                                        
                        
                                        #print 'Random Image ID: ', randImageID
                                        #print 'Random Image Name: ', randImageName
    
                                        randomImageBEURL = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(randImageID) + '/' + commandBirdsEye.postamble
    
                                        #print 'Random Birds Eye URL: ', randomImageBEURL
    
    
                    group = ({
                            'id': groupId,
                            'name': groupName,
                            'projectCount': projectCount,
                            'datasetCount': datasetCount,
                            'imageCount': groupImageCount,
                            'randomImageID': randImageID,
                            'randomImageName': randImageName,
                            'randomImageBEURL': randomImageBEURL
                            })
                    
                    group_list.append(group)
    
    
        prevgroup = ''
    
        new_group_list = list()
    
        for group in group_list:
    
            if prevgroup != group['id']:
            
                if group['imageCount'] > 0:
        
                    new_group_list.append(group)
                
                if userid == "":
        
                    new_group_list.append(group)
                
            prevgroup = group['id']
        
        for group in new_group_list:
            group_count = group_count + 1
    
        matrix_list = list()
        my_matrix_list = list()

        if request.user.is_superuser == True:
        
            matrix_list = matrix_list_not_by_user(request.user)
            my_matrix_list = matrix_list_by_user(request.user)
        
        else:
        
            matrix_list_1 = matrix_list_by_user(request.user)
            matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
            
            matrix_list = matrix_list_1 + matrix_list_2
            my_matrix_list = matrix_list_by_user(request.user)
            
        image_list = Image.objects.filter(owner=request.user).filter(active=True)
        server_list = Server.objects.all()

    
        data = { 'server': self, 'group_list': new_group_list, 'group_count': group_count, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list  }
    
        return data
    
    
    """
        Get the JSON Details for the Requested Group
    """
    def get_imaging_server_group_json(self, request, group_id):
    
        current_user = request.user
    
        commandAPI = Command.objects.filter(type=self.type).get(name='API')
        commandToken = Command.objects.filter(type=self.type).get(name='Token')
        commandLogin = Command.objects.filter(type=self.type).get(name='Login')
    
        commandGroupProjects = Command.objects.filter(type=self.type).get(name='GroupProjects')
        commandProjects = Command.objects.filter(type=self.type).get(name='Projects')
        commandProjectsDatasets = Command.objects.filter(type=self.type).get(name='ProjectDatasets')
        
        commandDatasetImages = Command.objects.filter(type=self.type).get(name='DatasetImages')
        commandBirdsEye = Command.objects.filter(type=self.type).get(name='BirdsEye')
        
        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'
        
        groups_url = commandGroupProjects.protocol.name + '://' + self.url_server + '/' + commandGroupProjects.application + '/' + commandGroupProjects.preamble
        projects_url = commandProjects.protocol.name + '://' + self.url_server + '/' + commandProjects.application + '/' + commandProjects.preamble + '/'
        datasets_url = commandProjectsDatasets.protocol.name + '://' + self.url_server + '/' + commandProjectsDatasets.application + '/' + commandProjectsDatasets.preamble + '/'
        
        images_url = commandDatasetImages.protocol.name + '://' + self.url_server + '/' + commandDatasetImages.application + '/' + commandDatasetImages.preamble + '/'
    
        #print "api_url", api_url
        #print "token_url", token_url
        #print "login_url", login_url
        
        session = requests.Session()
    
        try:
            r = session.get(api_url)
    
        except Exception as e:
            
            matrix_list = Matrix.objects.filter(owner=current_user)
            image_list = Image.objects.filter(owner=current_user).filter(active=True)
            server_list = Server.objects.all
    
            group_count = 0
            group_list = []
        
            data = { 'server': self, 'project_list': project_list, 'group': group, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }
    
            return data
    
        token = session.get(token_url).json()['data']
        session.headers.update({'X-CSRFToken': token, 'Referer': login_url})
        
        userid = self.uid
    
        cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
        password = cipher.decrypt(self.pwd)
    
        memberOfGroup_list = list()
        
        group_list = list()
        
        groupCount = 0
        
        if userid == "":
    
            project_url = groups_url + group_id + commandGroupProjects.postamble
            #print project_url
    
            payload = {'limit': 50}
            project_rsp = session.get(project_url, params=payload)
            project_data = project_rsp.json()
            
            #print 'project_rsp.status_code', project_rsp.status_code
    
            if project_rsp.status_code == 200:
    
                #print 'project_data', project_data
    
                project_meta = project_data['meta']
                projectCount = project_meta['totalCount']
    
                for p in project_data['data']:
    
                    details = p['omero:details']
    
                    groupdetails = details['group']
    
                    groupId = groupdetails['@id']
                    
                    if str(groupId) == group_id:
        
                        group_list.append(groupId)
                
                prevgroup = ''
    
                new_group_list = list()
    
                for group in group_list:
    
                    if prevgroup != group:
    
                        new_group_list.append(group)
        
                    prevgroup = group
                
                memberOfGroup_list = new_group_list
        
    
        if userid != "":
        
            payload = {'username': userid, 'password': password, 'server': 1}
        
            r = session.post(login_url, data=payload)
            login_rsp = r.json()
            try:
                assert r.status_code == 200
                assert login_rsp['success']
        
            except AssertionError:
        
                matrix_list = Matrix.objects.filter(owner=current_user)
                image_list = Image.objects.filter(owner=current_user).filter(active=True)
                server_list = Server.objects.all
    
                groupCount = 0
                group_list = []
        
                data = { 'server': self, 'project_list': project_list, 'group': group, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }
    
                return data
        
            eventContext = login_rsp['eventContext']
            memberOfGroups = eventContext['memberOfGroups']
            
            memberOfGroup_list = memberOfGroups
    
        #print 'memberOfGroup_list', memberOfGroup_list    
        
        project_list = list()
        group_list = list()
        group = ''
        
        for mog in memberOfGroup_list:
        
            if str(mog) == group_id:
    
                project_url = groups_url + str(group_id) + commandGroupProjects.postamble
                #project_url = projects_url + str(group_id)
                #project_url = group_url
                #print 'project_url', project_url
        
                payload = {'limit': 100}
                project_data = session.get(project_url, params=payload).json()
                assert len(project_data['data']) < 200
        
                project_meta = project_data['meta']
                projectCount = project_meta['totalCount']
                
                for p in project_data['data']:
                    
                    details = p['omero:details']
    
                    groupdetails = details['group']
    
                    group = ({
                        'id': groupdetails['@id'],
                        'name': groupdetails['Name'],
                        'projectCount': projectCount
                        })
                    
                    #print 'GROUP', group
        
                    group_list.append(group)
                    
                    #datasetCount = p['omero:childCount']
                    project_id = p['@id']
                    projectName = p['Name']
            
                    dataset_url = datasets_url + str(project_id) + '/' + commandProjectsDatasets.postamble
                    #dataset_url = datasets_url + str(project_id)
                    #print 'dataset_url', dataset_url
    
                    payload = {'limit': 100}
                    #dataset_data = session.get(dataset_url, params=payload).json()
                    dataset_rsp = session.get(dataset_url, params=payload)
                    dataset_data = dataset_rsp.json()        
                    #assert len(dataset_data['data']) < 100000
                    
                    imageCount = 0
                    datasetCount = 0
            
                    randImageID = ''
                    randImageName = ''
                    randomImageBEURL = ''
    
                    randImageID = '999999'
                    randImageName = 'NONE'
                    randomImageBEURL = 'NONE'            
    
                    if dataset_rsp.status_code == 200:
                    
                        dataset_meta = dataset_data['meta']
                        datasetMetaCount = dataset_meta['totalCount']
                    
                        if datasetMetaCount > 0:
        
                            for d in dataset_data['data']:
                                dataset_id = d['@id']
                                num_images = d['omero:childCount']
                                imageCount = imageCount + num_images
                
                                datasetCount = datasetCount + 1
        
                                image_url = images_url + str(dataset_id) + '/' + commandDatasetImages.postamble
                                #print 'image_url', image_url
        
                                #randImageIndex = randint(0, (imageCount - 1))
                                randImageIndex = 0
        
                                count = 0
                
                                if datasetCount == 1:
                
                                    payload = {'limit': 100}
                                    image_data = session.get(image_url, params=payload).json()
                                    assert len(dataset_data['data']) < 1000
                
                                    for i in image_data['data']:
                    
                                        if count == randImageIndex:
                                            randImageID = i['@id']
                                            randImageName = i['Name']
        
                                        count = count + 1
                        
                                    randomImageBEURL = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(randImageID) + '/' + commandBirdsEye.postamble
        
                    project = ({
                        'id': project_id,
                        'name': projectName,
                        'datasetCount': datasetCount,
                        'imageCount': imageCount,
                        'randomImageID': randImageID,
                        'randomImageName': randImageName,
                        'randomImageBEURL': randomImageBEURL
                    })
    
                    #print 'PROJECT', project
            
                    project_list.append(project)
    
        project_count = 0                    
        for project in project_list:
            project_count = project_count + 1
        
        matrix_list = list()
        my_matrix_list = list()

        if request.user.is_superuser == True:
        
            matrix_list = matrix_list_not_by_user(request.user)
            my_matrix_list = matrix_list_by_user(request.user)
        
        else:
        
            matrix_list_1 = matrix_list_by_user(request.user)
            matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
            
            matrix_list = matrix_list_1 + matrix_list_2
            my_matrix_list = matrix_list_by_user(request.user)
            
        image_list = Image.objects.filter(owner=request.user).filter(active=True)
        server_list = Server.objects.all()


        group = group_list[0]
        
        data = { 'server': self, 'project_count': project_count, 'project_list': project_list, 'group': group, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list  }
    
        return data
    
    
    """
        Get the JSON Details for the Requested Project
    """
    def get_imaging_server_project_json(self, request, project_id):
        
        current_user = request.user
    
        commandAPI = Command.objects.filter(type=self.type).get(name='API')
        commandToken = Command.objects.filter(type=self.type).get(name='Token')
        commandLogin = Command.objects.filter(type=self.type).get(name='Login')
    
        commandProjects = Command.objects.filter(type=self.type).get(name='Projects')
        commandProjectsDatasets = Command.objects.filter(type=self.type).get(name='ProjectDatasets')
        
        commandDatasetImages = Command.objects.filter(type=self.type).get(name='DatasetImages')
        commandBirdsEye = Command.objects.filter(type=self.type).get(name='BirdsEye')
    
        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'
        
        projects_url = commandProjects.protocol.name + '://' + self.url_server + '/' + commandProjects.application + '/' + commandProjects.preamble + '/'
        datasets_url = commandProjectsDatasets.protocol.name + '://' + self.url_server + '/' + commandProjectsDatasets.application + '/' + commandProjectsDatasets.preamble + '/'
        
        images_url = commandDatasetImages.protocol.name + '://' + self.url_server + '/' + commandDatasetImages.application + '/' + commandDatasetImages.preamble + '/'
    
        #print "api_url", api_url
        #print "token_url", token_url
        #print "login_url", login_url
        
        session = requests.Session()
    
        try:
            r = session.get(api_url)
    
        except Exception as e:
        
            matrix_list = Matrix.objects.filter(owner=current_user)
            image_list = Image.objects.filter(owner=current_user).filter(active=True)
            server_list = Server.objects.all
    
            group = ''
            project = ''
            dataset_list = []
        
            data = { 'server': self, 'group': group, 'project': project, 'dataset_list': dataset_list, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list }
        
            return data
    
        token = session.get(token_url).json()['data']
        session.headers.update({'X-CSRFToken': token, 'Referer': login_url})
        
        userid = self.uid
    
        cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
        password = cipher.decrypt(self.pwd)
    
        if userid != "":
    
            payload = {'username': userid, 'password': password, 'server': 1}
        
            r = session.post(login_url, data=payload)
            login_rsp = r.json()
            assert r.status_code == 200
            assert login_rsp['success']
    
    
        project_url = projects_url + project_id + '/' + commandProjects.postamble
        dataset_url = projects_url + project_id + '/' + commandProjectsDatasets.postamble
    
        #print project_url
        #print dataset_url
    
        payload = {'limit': 100}
        datasets_data = session.get(dataset_url, params=payload).json()
        assert len(datasets_data['data']) < 1000
    
        payload = {'limit': 100}
        project_data = session.get(project_url, params=payload).json()
        assert len(project_data['data']) < 1000
    
        pdata = project_data['data']
    
        name = pdata['Name']
        dataset_id = pdata['@id']
        datasetCount = pdata['omero:childCount']
        omerodetails = pdata['omero:details']
        group = omerodetails['group']
        groupname = group['Name']
        group_id = group['@id']
    
        group = ({
                    'id': group_id,
                    'name': groupname,
                    })
                
        project = ({
                    'id': dataset_id,
                    'name': name,
                    'datasetCount': datasetCount,
                    })
                
        dataset_list = list()
    
        randImageID = ''
        randImageName = ''
        randomImageBEURL = ''
                
        ddata = datasets_data['data']
    
        for d in ddata:
        
            dataset_id = d['@id']
            datasetName = d['Name']
            imageCount = d['omero:childCount']
            
            image_url = images_url + str(dataset_id) + '/' + commandDatasetImages.postamble
        
            #randImageIndex = randint(0, (imageCount - 1))
            randImageIndex = 0
    
            count = 0
                
            payload = {'limit': 100}
            image_data = session.get(image_url, params=payload).json()
            assert len(image_data['data']) < 200
                
            for i in image_data['data']:
                    
                if count == randImageIndex:
                    randImageID = i['@id']
                    randImageName = i['Name']
        
                count = count + 1
                        
            randomImageBEURL = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(randImageID) + '/' + commandBirdsEye.postamble
    
            dataset = ({
                        'id': dataset_id, 
                        'name': datasetName, 
                        'imageCount': imageCount,
                        'randomImageID': randImageID,
                        'randomImageName': randImageName,
                        'randomImageBEURL': randomImageBEURL
                        })
                        
            #print 'dataset', dataset
    
            dataset_list.append(dataset)
    
        matrix_list = list()
        my_matrix_list = list()

        if request.user.is_superuser == True:
        
            matrix_list = matrix_list_not_by_user(request.user)
            my_matrix_list = matrix_list_by_user(request.user)
        
        else:
        
            matrix_list_1 = matrix_list_by_user(request.user)
            matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
            
            matrix_list = matrix_list_1 + matrix_list_2
            my_matrix_list = matrix_list_by_user(request.user)
            
        image_list = Image.objects.filter(owner=request.user).filter(active=True)
        server_list = Server.objects.all()

        
        data = { 'server': self, 'group': group, 'project': project, 'dataset_list': dataset_list, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list }
        
        return data
    
    
    """
        Get the JSON Details for the Requested Dataset
    """
    def get_imaging_server_dataset_json(self, request, dataset_id):
        
        current_user = request.user
    
        userid = self.uid
    
        cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
        password = cipher.decrypt(self.pwd)
    
        if userid == "":
            commandViewer = Command.objects.filter(type=self.type).get(name='PublicViewer')
        else:
            commandViewer = Command.objects.filter(type=self.type).get(name='Viewer')
    
        commandAPI = Command.objects.filter(type=self.type).get(name='API')
        commandToken = Command.objects.filter(type=self.type).get(name='Token')
        commandLogin = Command.objects.filter(type=self.type).get(name='Login')
    
        commandDataset = Command.objects.filter(type=self.type).get(name='Dataset')
        commandDatasetProjects = Command.objects.filter(type=self.type).get(name='DatasetProjects')
        commandDatasetImages = Command.objects.filter(type=self.type).get(name='DatasetImages')
    
        commandThumbnail = Command.objects.filter(type=self.type).get(name='Thumbnail')
        commandBirdsEye = Command.objects.filter(type=self.type).get(name='BirdsEye')
        
        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'
        
        datasets_url = commandDataset.protocol.name + '://' + self.url_server + '/' + commandDataset.application + '/' + commandDataset.preamble + '/'
        projects_url = commandDatasetProjects.protocol.name + '://' + self.url_server + '/' + commandDatasetProjects.application + '/' + commandDatasetProjects.preamble + '/'
        images_url = commandDatasetImages.protocol.name + '://' + self.url_server + '/' + commandDatasetImages.application + '/' + commandDatasetImages.preamble + '/'
        
        #print "api_url", api_url
        #print "token_url", token_url
        #print "login_url", login_url
        
        session = requests.Session()
    
        try:
            r = session.get(api_url)
    
        except Exception as e:
            
            matrix_list = Matrix.objects.filter(owner=current_user)
            image_list = Image.objects.filter(owner=current_user).filter(active=True)
            server_list = Server.objects.all
    
            dataset = ''
            group = ''
            images_list = []
            project_list = []
        
            data = { 'server': self, 'group': group, 'projects': project_list, 'images': images_list, 'dataset': dataset, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list }
        
            return data
    
        token = session.get(token_url).json()['data']
        session.headers.update({'X-CSRFToken': token, 'Referer': login_url})
        
        if userid != "":
        
            payload = {'username': userid, 'password': password, 'server': 1}
        
            r = session.post(login_url, data=payload)
            login_rsp = r.json()
            assert r.status_code == 200
            assert login_rsp['success']
    
        
        dataset_url = datasets_url + dataset_id + '/' + commandDataset.postamble
        projects_url = projects_url + dataset_id + '/' + commandDatasetProjects.postamble
        images_url = datasets_url + dataset_id + '/'+ commandDatasetImages.postamble
        
        #print dataset_url
        #print projects_url
        #print images_url
    
        payload = {'limit': 100}
        images_data = session.get(images_url, params=payload).json()
        assert len(images_data['data']) < 200
        
        payload = {'limit': 100}
        dataset_data = session.get(dataset_url, params=payload).json()
        assert len(dataset_data['data']) < 200
        
        payload = {'limit': 100}
        projects_data = session.get(projects_url, params=payload).json()
        assert len(projects_data['data']) < 200
        
        ddata = dataset_data['data']
        idata = images_data['data']
        pdata = projects_data['data']
        
        name = ddata['Name']
        dataset_id = ddata['@id']
        imageCount = ddata['omero:childCount']
        
        dataset = ({
                    'id': dataset_id,
                    'name': name,
                    'imageCount': imageCount
                    })
        
        project_list = list()
        
        group_id = ''
        groupname = ''
        
        for p in pdata:
            project = ({'id': p['@id'], 'name': p['Name']})
            project_list.append(project)
            omerodetails = p['omero:details']
            groupdetails = omerodetails['group']
            groupname = groupdetails['Name']
            group_id = groupdetails['@id']
    
        group = ({
                    'id': group_id,
                    'name': groupname,
                    })
        
        images_list = list()
        
        for i in idata:
        
            image_id = str(i['@id'])
            image_name = i['Name']
            
            if userid == "":
                image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + commandViewer.application + '/' + commandViewer.preamble + '/' + image_id
            else:
                image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + commandViewer.application + '/' + commandViewer.preamble + image_id
    
            image_birdseye_url = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + image_id + '/' + commandBirdsEye.postamble
            image_thumbnail_url = commandThumbnail.protocol.name + '://' + self.url_server + '/' + commandThumbnail.application + '/' + commandThumbnail.preamble + '/' + image_id 
    
            image = ({
                'id': image_id, 
                'name': image_name,
                'viewer_url': image_viewer_url,
                'birdseye_url': image_birdseye_url,
                'thumbnail_url': image_thumbnail_url
                })
                
            images_list.append(image)
            
        matrix_list = list()
        my_matrix_list = list()

        if request.user.is_superuser == True:
        
            matrix_list = matrix_list_not_by_user(request.user)
            my_matrix_list = matrix_list_by_user(request.user)
        
        else:
        
            matrix_list_1 = matrix_list_by_user(request.user)
            matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
            
            matrix_list = matrix_list_1 + matrix_list_2
            my_matrix_list = matrix_list_by_user(request.user)
            
        image_list = Image.objects.filter(owner=request.user).filter(active=True)
        server_list = Server.objects.all()

        
        data = { 'server': self, 'group': group, 'projects': project_list, 'images': images_list, 'dataset': dataset, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list }
        
        return data
    
    
    """
        Get the JSON Details for the Requested Image
    """
    def get_imaging_server_image_json(self, request, image_id):
        
        current_user = request.user
    
        userid = self.uid
    
        cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
        password = cipher.decrypt(self.pwd)
    
        commandAPI = Command.objects.filter(type=self.type).get(name='API')
        commandToken = Command.objects.filter(type=self.type).get(name='Token')
        commandLogin = Command.objects.filter(type=self.type).get(name='Login')
    
        commandImages = Command.objects.filter(type=self.type).get(name='Images')
        commandImageDatasets = Command.objects.filter(type=self.type).get(name='ImageDatasets')
        commandImageROIs = Command.objects.filter(type=self.type).get(name='ImageROIs')
    
        commandDatasetProjects = Command.objects.filter(type=self.type).get(name='DatasetProjects')
    
        commandViewer = ''
        
        if userid == "":
            commandViewer = Command.objects.filter(type=self.type).get(name='PublicViewer')
        else:
            commandViewer = Command.objects.filter(type=self.type).get(name='Viewer')
        
        commandBirdsEye = Command.objects.filter(type=self.type).get(name='BirdsEye')
        commandRegion = Command.objects.filter(type=self.type).get(name='Region')
    
        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'
        
        images_url = commandImages.protocol.name + '://' + self.url_server + '/' + commandImages.application + '/' + commandImages.preamble + '/'
        datasets_url = commandImageDatasets.protocol.name + '://' + self.url_server + '/' + commandImageDatasets.application + '/' + commandImageDatasets.preamble + '/'
        imagerois_url = commandImageROIs.protocol.name + '://' + self.url_server + '/' + commandImageROIs.application + '/' + commandImageROIs.preamble + '/'
        
        projects_url = commandDatasetProjects.protocol.name + '://' + self.url_server + '/' + commandDatasetProjects.application + '/' + commandDatasetProjects.preamble + '/'
    
        if userid == "":
            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + commandViewer.application + '/' + commandViewer.preamble + '/' + image_id
        else:
            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + commandViewer.application + '/' + commandViewer.preamble + image_id
    
        image_birdseye_url = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + image_id + '/' + commandBirdsEye.postamble
    
        image_region_url = commandRegion.protocol.name + '://' + self.url_server + '/' + commandRegion.application + '/' + commandRegion.preamble + '/' + image_id + '/' + commandRegion.postamble
        
        #print "image_viewer_url", image_viewer_url
        #print "image_birdseye_url", image_birdseye_url
        
        #print "api_url", api_url
        #print "token_url", token_url
        #print "login_url", login_url
        
        session = requests.Session()
    
        try:
            r = session.get(api_url)
    
        except Exception as e:
            
            matrix_list = Matrix.objects.filter(owner=current_user)
            image_list = Image.objects.filter(owner=current_user).filter(active=True)
            server_list = Server.objects.all
    
            group_count = 0
            group_list = []
        
            data = { 'server': self, 'group': group, 'projects': projects, 'datasets': datasets, 'image': image, 'rois': roi_list, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list }
        
            return data
    
        token = session.get(token_url).json()['data']
        session.headers.update({'X-CSRFToken': token, 'Referer': login_url})
        
        if userid != "":
            payload = {'username': userid, 'password': password, 'server': 1}
        
            r = session.post(login_url, data=payload)
            login_rsp = r.json()
            assert r.status_code == 200
            assert login_rsp['success']
    
    
        rois_url = imagerois_url + image_id + '/' + commandImageROIs.postamble
        #print rois_url
        
        payload = {'limit': 100}
        rois_data = session.get(rois_url, params=payload).json()
        assert len(rois_data['data']) < 200
        
        rmeta = rois_data['meta']
        roiCount = rmeta['totalCount']
        
        rdata = rois_data['data']
        
        roi_list = list()
        
        for r in rdata:
            shapes = r['shapes']
            roi_id = r['@id']
        
            shape_list = list()
        
            for s in shapes:
                shape_id = s['@id']
                shape_type = s['@type']
                
                types = shape_type.split('#')
                #print 'types', types
                type = types[1]
                
                coordX = ''
                coordY = ''
                centreX = ''
                centreY = ''
                width = '0'
                height = '0'
                
                #print 'type', type
                
                if type == 'Point':
        
                    centreX = s['X']
                    centreY = s['Y']
                    intCoordX = int(s['X'])
                    intCoordY = int(s['Y'])
                    intHalf = 3192 / 2
                    intWidth = intHalf
                    intHeight = intHalf
            
                    intNewCoordX = intCoordX - intWidth
                    intNewCoordY = intCoordY - intHeight
                    
                    coordX = str(intNewCoordX)
                    coordY = str(intNewCoordY)
                    width = str( 3192 )
                    height = str( 3192 )
            
                if type == 'Rectangle':
        
                    centreX = s['X']
                    centreY = s['Y']
                    intCoordX = int(s['X'])
                    intCoordY = int(s['Y'])
                    intWidth = int(s['Width'])
                    intHeight = int(s['Height'])
            
                    coordX = str(intCoordX)
                    coordY = str(intCoordY)
                    width = str(intWidth)
                    height = str(intHeight)
                    
                if type == 'Ellipse':
        
                    centreX = s['X']
                    centreY = s['Y']
                    oldCoordX = s['X']
                    oldCoordY = s['Y']
                    radiusX = s['RadiusX']
                    radiusY = s['RadiusY']
                    intX = int(oldCoordX)
                    intY = int(oldCoordY)
                    intRadiusX = int(radiusX)
                    intRadiusY = int(radiusY)
                    intWidth = intRadiusX * 2
                    intHeight = intRadiusY * 2
                    intCoordX = intX - intRadiusX
                    intCoordY = intY - intRadiusY
        
                    coordX = str(intCoordX)
                    coordY = str(intCoordY)
                    width = str(intWidth)
                    height = str(intHeight)
        
                if type == 'Polygon':
        
                    points = s['Points']
                    points_array = points.split(' ')
        
                    x_list = list()
                    y_list = list()
                    
                    for XandY in points_array:
                        XandYSplit = XandY.split(',')
                        strX = XandYSplit[0].split('.')
                        strY = XandYSplit[1].split('.')
                    
                        x_list.append(int(strX[0]))
                        y_list.append(int(strY[0]))
        
                    maxX = max(x_list)            
                    minX = min(x_list)            
                    maxY = max(y_list)            
                    minY = min(y_list)            
        
                    coordX = str(minX)
                    coordY = str(minY)
                    centreX = coordX
                    centreY = coordY
                    
                    intWidth = maxX - minX
                    intHeight = maxY - minY
                    
                    width = str(intWidth)
                    height = str(intHeight)
                
                if type == 'Polyline':
        
                    points = s['Points']
                    points_array = points.split(' ')
        
                    x_list = list()
                    y_list = list()
                    
                    for XandY in points_array:
                        XandYSplit = XandY.split(',')
                        strX = XandYSplit[0].split('.')
                        strY = XandYSplit[1].split('.')
                    
                        x_list.append(int(strX[0]))
                        y_list.append(int(strY[0]))
        
                    maxX = max(x_list)            
                    minX = min(x_list)            
                    maxY = max(y_list)            
                    minY = min(y_list)            
        
                    coordX = str(minX)
                    coordY = str(minY)
                    centreX = coordX
                    centreY = coordY
                    
                    intWidth = maxX - minX
                    intHeight = maxY - minY
                    
                    width = str(intWidth)
                    height = str(intHeight)
                
                if int(width) > 3192 or int(height) > 3192:
                
                    middleX = int(coordX) + ( int(width) / 2 )
                    middleY = int(coordY) + ( int(height) / 2 )
                
                    intX = middleX - ( 3192 / 2 )
                    intY = middleY - ( 3192 / 2 )
                
                    coordX = str(int(intX))
                    coordY = str(int(intY))
                    
                    width = "3192"
                    height = "3192"
    
                shape_url = image_region_url + coordX + ',' + coordY + ',' + width + ',' + height
                viewer_url = image_viewer_url + '&X=' + str(centreX) + '&Y=' + str(centreY) + '&ZM=25'
                
                shape = ({'id': shape_id, 'type': type, 'shape_url': shape_url, 'viewer_url': viewer_url, 'x': coordX, 'y': coordY, 'centre_x': centreX, 'centre_y': centreY, 'width': width, 'height': height })
                
                shape_list.append(shape)
            
            roi = ({'id': roi_id, 'shapes': shape_list})
        
            roi_list.append(roi)
    
    
        image_url = images_url + image_id
        #print image_url
    
        payload = {'limit': 100}
        image_data = session.get(image_url, params=payload).json()
        assert len(image_data['data']) < 200
        
        data = image_data['data']
        name = data['Name']
        description = data.get('Description', '')
        #description = data['Description']
        pixels = data['Pixels']
        type = pixels['Type']
        pixeltype = type['value']
        sizeX = pixels['SizeX']
        sizeY = pixels['SizeY']
        sizeZ = pixels['SizeZ']
        sizeT = pixels['SizeT']
        physicalsizeX = pixels.get('PhysicalSizeX', '')
        physicalsizeY = pixels.get('PhysicalSizeY', '')
    
        if physicalsizeX == '':
            pixelsizeX = ''
        else:
            pixelsizeX = physicalsizeX['Value']
    
        if physicalsizeY == '':
            pixelsizeY = ''
        else:
            pixelsizeY = physicalsizeY['Value']
    
        group_id = ''
        groupname = ''
        
        omerodetails = data['omero:details']
        groupdetails = omerodetails['group']
        groupname = groupdetails['Name']
        group_id = groupdetails['@id']
    
        group = ({
                    'id': group_id,
                    'name': groupname,
                    })
        
        image = ({
                    'id': image_id,
                    'name': name,
                    'description': description,
                    'sizeX': sizeX,
                    'sizeY': sizeY,
                    'pixeltype': pixeltype,
                    'pixelsizeX': pixelsizeX,
                    'pixelsizeY': pixelsizeY,
                    'sizeZ': sizeZ,
                    'sizeT': sizeT,
                    'roi_count': roiCount,
                    'viewer_url': image_viewer_url,
                    'birdseye_url': image_birdseye_url
                    })
    
        dataset_url = datasets_url + image_id + '/' + commandImageDatasets.postamble
        #print dataset_url
    
        payload = {'limit': 100}
        dataset_data = session.get(dataset_url, params=payload).json()
        assert len(dataset_data['data']) < 200
        
        ddata = dataset_data['data']
        
        datasets = list()
        projects = list()
        
        for p in ddata:
            dataset = ({'id': p['@id'], 'name': p['Name']})
            
            projects_url = projects_url + str(p['@id']) + '/' + commandDatasetProjects.postamble
            
            #print 'projects_url', projects_url
    
            payload = {'limit': 100}
            project_data = session.get(projects_url, params=payload).json()
            assert len(project_data['data']) < 200
    
            pdata = project_data['data']
    
            for p in pdata:
                project = ({'id': p['@id'], 'name': p['Name']})
                projects.append(project)
    
            datasets.append(dataset)
        
        matrix_list = list()
        my_matrix_list = list()

        if request.user.is_superuser == True:
        
            matrix_list = matrix_list_not_by_user(request.user)
            my_matrix_list = matrix_list_by_user(request.user)
        
        else:
        
            matrix_list_1 = matrix_list_by_user(request.user)
            matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
            
            matrix_list = matrix_list_1 + matrix_list_2
            my_matrix_list = matrix_list_by_user(request.user)
            
        image_list = Image.objects.filter(owner=request.user).filter(active=True)
        server_list = Server.objects.all()

        
        data = { 'server': self, 'group': group, 'projects': projects, 'datasets': datasets, 'image': image, 'rois': roi_list, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'server_list': server_list, 'image_list': image_list }
    
        return data
    

    """
        Check the JSON Details for the Requested Image on Wordpress
    """
    def check_wordpress_image(self, user, image_id):
        
        credential = Credential.objects.get(username=user.username)
    
        commandWordpressImage = Command.objects.filter(type=self.type).get(name='WordpressImage')
        
        image_url = commandWordpressImage.protocol.name + '://' + self.url_server + '/' + commandWordpressImage.application + '/' + commandWordpressImage.preamble + '/' + str(image_id)
        
        #print("image_url : " + image_url)
        
        token_str = credential.username + ':' + credential.apppwd
        encoded_token_str = token_str.encode('utf8')
        
        token = base64.standard_b64encode(encoded_token_str)
        headers = {'Authorization': 'Basic ' + token.decode('utf8')}
    
        data = {}
    
        try:
    
            response = requests.get(image_url, headers=headers, timeout=5)
    
            if response.status_code == requests.codes.ok:
            
                media_data = response.json()
                
                #print("media_data : " + str(media_data))
                
                caption = media_data['caption']
                caption_rendered = caption['rendered']
                
                title = media_data['title']
                title_rendered = title['rendered']
                
                description = media_data['alt_text']
    
                image_viewer_url = media_data['source_url']
                media_details = media_data['media_details']
                sizes = media_details['sizes']
                thumbnail = sizes['thumbnail']
                image_thumbnail_url = thumbnail['source_url']
                medium = sizes['medium']
                image_birdseye_url = medium['source_url']
    
                image = ({
                    'id': str(image_id),
                    'name': title_rendered,
                    'caption': caption_rendered[:-5][3:].rstrip(),
                    'description': description,
                    'viewer_url': image_viewer_url,
                    'birdseye_url': image_birdseye_url,
                    'thumbnail_url': image_thumbnail_url
                })
    
                data = image
    
            else:
    
                image = ({
                    'id': str(image_id),
                    'name': '',
                    'caption': '',
                    'description': '',
                    'viewer_url': '',
                    'birdseye_url': '',
                    'thumbnail_url': ''
                })
    
                data = image
    
        except Exception as e:
    
            #print('Exception!', e)
    
            image = ({
                'id': str(image_id),
                'name': '',
                'caption': '',
                'description': '',
                'viewer_url': '',
                'birdseye_url': '',
                'thumbnail_url': ''
            })
    
            data = image
    
        data = { 'image': image }

        #print("data : " + str(data))
        
        return data


    """
        Check the JSON Details for the Requested Image
    """
    def check_imaging_server_image(self, user, image_id):
        
        current_user = user

        userid = self.uid
    
        cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
        password = cipher.decrypt(self.pwd)
    
        commandAPI = Command.objects.filter(type=self.type).get(name='API')
        commandToken = Command.objects.filter(type=self.type).get(name='Token')
        commandLogin = Command.objects.filter(type=self.type).get(name='Login')
    
        commandImages = Command.objects.filter(type=self.type).get(name='Images')
        commandImageROIs = Command.objects.filter(type=self.type).get(name='ImageROIs')
    
        commandViewer = ''
        
        if userid == "":
            commandViewer = Command.objects.filter(type=self.type).get(name='PublicViewer')
        else:
            commandViewer = Command.objects.filter(type=self.type).get(name='Viewer')
        
        commandBirdsEye = Command.objects.filter(type=self.type).get(name='BirdsEye')
    
        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'
        
        images_url = commandImages.protocol.name + '://' + self.url_server + '/' + commandImages.application + '/' + commandImages.preamble + '/'
        imagerois_url = commandImageROIs.protocol.name + '://' + self.url_server + '/' + commandImageROIs.application + '/' + commandImageROIs.preamble + '/'
        
        if userid == "":
            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + commandViewer.application + '/' + commandViewer.preamble + '/' + str(image_id)
        else:
            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + commandViewer.application + '/' + commandViewer.preamble + str(image_id)
    
        image_birdseye_url = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(image_id) + '/' + commandBirdsEye.postamble
    
        session = requests.Session()
    
        try:
            r = session.get(api_url)
    
        except Exception as e:
            
            data = { 'image': image }
        
            return data
    
        token = session.get(token_url).json()['data']
        session.headers.update({'X-CSRFToken': token, 'Referer': login_url})
        
        if userid != "":
            payload = {'username': userid, 'password': password, 'server': 1}
        
            r = session.post(login_url, data=payload)
            login_rsp = r.json()
            assert r.status_code == 200
            assert login_rsp['success']
    
    
        rois_url = imagerois_url + str(image_id) + '/' + commandImageROIs.postamble
        #print rois_url
        
        payload = {'limit': 100}
        rois_data = session.get(rois_url, params=payload).json()
        assert len(rois_data['data']) < 200
        
        rmeta = rois_data['meta']
        roiCount = rmeta['totalCount']
        
        image_url = images_url + str(image_id)
        #print image_url
    
        try:
            payload = {'limit': 100}
            image_data = session.get(image_url, params=payload).json()
            assert len(image_data['data']) < 20
        
        except Exception as e:
        
            image = ({
                'id': "Not Found",
                'name': "",
                'description': "",
                'sizeX': "",
                'sizeY': "",
                'pixeltype': "",
                'pixelsizeX': "",
                'pixelsizeY': "",
                'sizeZ': "",
                'sizeT': "",
                'roi_count': "",
                'viewer_url': "",
                'birdseye_url': ""
                })
             
            data = { 'image': image }
             
            return data

        
        data = image_data['data']
        name = data['Name']
        description = data.get('Description', '')
        #description = data['Description']
        pixels = data['Pixels']
        type = pixels['Type']
        pixeltype = type['value']
        sizeX = pixels['SizeX']
        sizeY = pixels['SizeY']
        sizeZ = pixels['SizeZ']
        sizeT = pixels['SizeT']
        physicalsizeX = pixels.get('PhysicalSizeX', '')
        physicalsizeY = pixels.get('PhysicalSizeY', '')
    
        if physicalsizeX == '':
            pixelsizeX = ''
        else:
            pixelsizeX = physicalsizeX['Value']
    
        if physicalsizeY == '':
            pixelsizeY = ''
        else:
            pixelsizeY = physicalsizeY['Value']
    
        image = ({
                    'id': str(image_id),
                    'name': name,
                    'description': description,
                    'sizeX': sizeX,
                    'sizeY': sizeY,
                    'pixeltype': pixeltype,
                    'pixelsizeX': pixelsizeX,
                    'pixelsizeY': pixelsizeY,
                    'sizeZ': sizeZ,
                    'sizeT': sizeT,
                    'roi_count': roiCount,
                    'viewer_url': image_viewer_url,
                    'birdseye_url': image_birdseye_url
                    })
    
        data = { 'image': image }
    
        return data
    

    """
        Check the JSON Details for the Requested Image ROI
    """
    def check_imaging_server_image_roi(self, user, image_id, in_roi_id):
        
        current_user = user
        
        userid = self.uid
    
        cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
        password = cipher.decrypt(self.pwd)
    
        commandAPI = Command.objects.filter(type=self.type).get(name='API')
        commandToken = Command.objects.filter(type=self.type).get(name='Token')
        commandLogin = Command.objects.filter(type=self.type).get(name='Login')
    
        commandImageROIs = Command.objects.filter(type=self.type).get(name='ImageROIs')
    
        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'
        
        imagerois_url = commandImageROIs.protocol.name + '://' + self.url_server + '/' + commandImageROIs.application + '/' + commandImageROIs.preamble + '/'
    
        session = requests.Session()
    
        roi = ({'id': "" })
        
        try:
            r = session.get(api_url)
    
        except Exception as e:
            
            data = { 'roi': roi }
        
            return data
    
        token = session.get(token_url).json()['data']
        session.headers.update({'X-CSRFToken': token, 'Referer': login_url})
        
        if userid != "":
            payload = {'username': userid, 'password': password, 'server': 1}
        
            r = session.post(login_url, data=payload)
            login_rsp = r.json()
            assert r.status_code == 200
            assert login_rsp['success']
    
    
        rois_url = imagerois_url + str(image_id) + '/' + commandImageROIs.postamble
        #print("rois_url : " + rois_url)
        
        payload = {'limit': 100}
        rois_data = session.get(rois_url, params=payload).json()
        assert len(rois_data['data']) < 200
        
        rmeta = rois_data['meta']
        roiCount = rmeta['totalCount']
        
        #print("roiCount : " + str(roiCount))
        
        #if roiCount == 0:
        
            #roi = ({'id': 0 })
            
            #data = { 'roi': roi }

        #else:
        
        rdata = rois_data['data']
        
        for r in rdata:
            roi_id = r['@id']
            
            if in_roi_id == roi_id:
        
                roi = ({'id': roi_id })
        
        data = { 'roi': roi }
    
        #print("data : " + str(data))

        return data
    
        
class Command(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    application = models.CharField(max_length=25, blank=True, default='')
    preamble = models.CharField(max_length=50, blank=True, default='')
    postamble = models.CharField(max_length=50, blank=True, default='')
    protocol = models.ForeignKey(Protocol, default=0, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, related_name='commands', default=0, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='commands', on_delete=models.DO_NOTHING)

    @classmethod
    def create(cls, name, application, preamble, postamble, protocol, type, owner):
        return cls(name=name, application=application, preamble=preamble, postamble=postamble, protocol=protocol, type=type, owner=owner)
    
    def __str__(self):
        return f"{self.id}, {self.name}, {self.application}, {self.preamble}, {self.postamble}, {self.protocol.id}, {self.type.id}, {self.owner.id}"
        
    def __repr__(self):
        return f"{self.id}, {self.name}, {self.application}, {self.preamble}, {self.postamble}, {self.protocol.id}, {self.type.id}, {self.owner.id}"
       

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user
        

class Image(models.Model):    
    identifier = models.IntegerField(default=0)
    name = models.CharField(max_length=255, blank=False, default='')
    server = models.ForeignKey(Server, related_name='images', default=0, on_delete=models.CASCADE)
    viewer_url = models.CharField(max_length=255, blank=False, default='')
    birdseye_url = models.CharField(max_length=255, blank=False, default='')
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    roi = models.IntegerField(default=0)
    
    @classmethod
    def create(cls, identifier, name, server, viewer_url, birdseye_url, active, roi, owner):
        return cls(identifier=identifier, name=name, server=server, viewer_url=viewer_url, birdseye_url=birdseye_url, active=active, roi=roi, owner=owner)
    
    def __str__(self):
        return f"{self.id}, {self.identifier}, {self.name}, {self.server.id}, {self.viewer_url}, {self.birdseye_url}, {self.owner.id}, {self.active}, {self.roi}"
        
    def __repr__(self):
        return f"{self.id}, {self.identifier}, {self.name}, {self.server.id}, {self.viewer_url}, {self.birdseye_url}, {self.owner.id}, {self.active}, {self.roi}"


    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user
        
    def set_active(self):
        self.active = True
        
    def set_inactive(self):
        self.active = False
        
    def is_active(self):
        if self.active == True:
            return True
        else:
            return False

    def is_inactive(self):
        if self.active == False:
            return True
        else:
            return False
    
    def is_omero_image(self):
        if "iviewer" in self.viewer_url:
            return True
        else:
            return False

    def is_non_omero_image(self):
        if "iviewer" in self.viewer_url:
            return False
        else:
            return True
    
    def is_duplicate(self, a_identifier, a_name, a_server, a_viewer_url, a_birdseye_url, a_active, a_roi, a_owner):
    
        if self.identifier == a_identifier and self.name == a_name and self.server == a_server and self.viewer_url == a_viewer_url and self.birdseye_url == a_birdseye_url and self.active == a_active and self.roi == a_roi and self.owner == a_owner:
            return True
        else:
            return False
    
    def image_id(self):

        return self.identifier


class Cell(models.Model):
    matrix = models.ForeignKey(Matrix, related_name='bench_cells', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=4095, default='')
    xcoordinate = models.IntegerField(default=0)
    ycoordinate = models.IntegerField(default=0)
    blogpost = models.CharField(max_length=50, blank=True, default='')
    image = models.ForeignKey(Image, null=True, related_name='image', on_delete=models.CASCADE)

    @classmethod
    def create(cls, matrix, title, description, xcoordinate, ycoordinate, blogpost, image):
        return cls(matrix=matrix, title=title, description=description, xcoordinate=xcoordinate, ycoordinate=ycoordinate, blogpost=blogpost, image=image)
    
    def __str__(self):
        str_image = ""

        if self.has_image() == True:
            str_image = self.image.id
        else:
            str_image = "None"
        
        return f"{self.id}, {self.matrix.id}, {self.title}, {self.description}, {self.xcoordinate}, {self.ycoordinate}, {self.blogpost}, {str_image}"

    def __repr__(self):
        str_image = ""

        if self.has_image() == True:
            str_image = self.image.id
        else:
            str_image = "None"
        
        return f"{self.id}, {self.matrix.id}, {self.title}, {self.description}, {self.xcoordinate}, {self.ycoordinate}, {self.blogpost}, {str_image}"

    def is_header(self):
        if self.xcoordinate == 0 or self.ycoordinate == 0:
            return True
        else:
            return False
            
    def is_column_header(self):
        if self.xcoordinate == 0:
            return True
        else:
            return False
            
    def is_row_header(self):
        if self.ycoordinate == 0:
            return True
        else:
            return False
            
    def is_master(self):
        if self.xcoordinate == 0 and self.ycoordinate == 0:
            return True
        else:
            return False

    def set_blogpost(self, a_blogpost):
        self.blogpost = a_blogpost

    def has_no_blogpost(self):
        if self.blogpost == '' or self.blogpost == '0':
            return True
        else:
            return False
            
    def has_blogpost(self):
        if self.blogpost == '' or self.blogpost == '0':
            return False
        else:
            return True
            
    def has_no_image(self):
        if self.image is None:
            return True
        else:
            return False
            
    def has_image(self):
        if self.image is None:
            return False
        else:
            return True
            
    def set_matrix(self, a_matrix):
        self.matrix = a_matrix

    def set_xcoordinate(self, a_column):
        self.xcoordinate = a_column

    def set_ycoordinate(self, a_row):
        self.ycoordinate = a_row

    def increment_x(self):
        self.xcoordinate += 1
        
    def increment_y(self):
        self.ycoordinate += 1
        
    def decrement_x(self):
        self.xcoordinate -= 1
        
    def decrement_y(self):
        self.ycoordinate -= 1
        

class Blog(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    protocol = models.ForeignKey(Protocol, related_name='blogs', default=0, on_delete=models.CASCADE)
    url_blog = models.CharField(max_length=50, blank=False, default='')
    application = models.CharField(max_length=25, blank=True, default='')
    preamble = models.CharField(max_length=50, blank=True, default='')
    postamble = models.CharField(max_length=50, blank=True, default='')
    owner = models.ForeignKey(User, related_name='blogs', on_delete=models.DO_NOTHING)
    
    @classmethod
    def create(cls, name, protocol, url_blog, application, preamble, postamble, owner):
        return cls(name=name, protocol=protocol, url_blog=url_blog, application=application, preamble=preamble, postamble=postamble, owner=owner)
    
    def __str__(self):
        return f"{self.id}, {self.name}, {self.protocol.id}, {self.url_blog}, {self.application}, {self.preamble}, {self.postamble}, {self.owner.id}"

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.protocol.id}, {self.url_blog}, {self.application}, {self.preamble}, {self.postamble}, {self.owner.id}"

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user
        

class Credential(models.Model):
    username = models.CharField(max_length=50, blank=False, unique=True)
    wordpress = models.IntegerField(default=0, blank=False)
    apppwd = models.CharField(max_length=50, blank=True, default='')
    owner = models.ForeignKey(User, related_name='credentials', on_delete=models.DO_NOTHING)
    
    @classmethod
    def create(cls, username, wordpress, apppwd, owner):
        return cls(username=username, wordpress=wordpress, apppwd=apppwd, owner=owner)
    
    def __str__(self):
        return f"{self.id}, {self.username}, {self.wordpress}, {self.apppwd}, {self.owner.id}"

    def __repr__(self):
        return f"{self.id}, {self.username}, {self.wordpress}, {self.apppwd}, {self.owner.id}"

    def has_no_apppwd(self):
        if self.apppwd == '':
            return True
        else:
            return False
            
    def has_apppwd(self):
        if self.apppwd == '':
            return False
        else:
            return True
            
    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user



"""
    Get a Blog Post from Wordpress
"""
def get_a_post_from_wordpress(user_name, post_id):

    credential = Credential.objects.get(username=user_name)

    blogGetPost = Blog.objects.get(name='GetPost')

    get_post_url = blogGetPost.protocol.name + '://' + blogGetPost.url_blog + '/' + blogGetPost.application + '/' + blogGetPost.preamble + '/' + post_id

    #print("get_post_url : ", get_post_url)

    try:
        response = requests.get(get_post_url)

        response.raise_for_status()
        
        post_id = str(json.loads(response.content)['id'])
        
    except HTTPError as http_err:
        
        #print(f'get_a_post_from_wordpress - HTTP error occurred: {http_err}')
        
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

        #print(f'get_a_post_from_wordpress - Other error occurred: {err}')

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

        #print('get_a_post_from_wordpress - Success!')

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
def get_a_post_comments_from_wordpress(post_id):

    blogGetPostComments = Blog.objects.get(name='GetPostComments')

    get_post_comments_url = blogGetPostComments.protocol.name + '://' + blogGetPostComments.url_blog + '/' + blogGetPostComments.application + '/' + blogGetPostComments.preamble + post_id
    
    #print("get_post_comments_url : ", get_post_comments_url)

    comment_list = list()

    try:
        response = requests.get(get_post_comments_url)

        response.raise_for_status()
                
    except HTTPError as http_err:
        
        #print(f'get_a_post_comments_from_wordpress - HTTP error occurred: {http_err}')

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

        #print(f'get_a_post_comments_from_wordpress - Other error occurred: {err}')

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

        #print('get_a_post_comments_from_wordpress - Success!')

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


class Authority(models.Model):
    name = models.CharField(max_length=12, blank=False, unique=True, default='')
    owner = models.ForeignKey(User, related_name='authorities', on_delete=models.DO_NOTHING)

    @classmethod
    def create(cls, name, owner):
        return cls(name=name, owner=owner)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.owner.id}"

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False
            
    def set_owner(self, a_user):
        self.owner = a_user

    def set_as_none(self):
        self.name = 'NONE'

    def set_as_editor(self):
        self.name = 'EDITOR'

    def set_as_viewer(self):
        self.name = 'VIEWER'

    def set_as_owner(self):
        self.name = 'OWNER'

    def set_as_admin(self):
        self.name = 'ADMIN'

    def is_none(self):
        if self.name == 'NONE':
            return True
        else:
            return False
            
    def is_editor(self):
        if self.name == 'EDITOR':
            return True
        else:
            return False
            
    def is_viewer(self):
        if self.name == 'VIEWER':
            return True
        else:
            return False

    def is_owner(self):
        if self.name == 'OWNER':
            return True
        else:
            return False
        
    def is_admin(self):
        if self.name == 'ADMIN':
            return True
        else:
            return False
        

class Authorisation(models.Model):
    matrix = models.ForeignKey(Matrix, related_name='authorisations', on_delete=models.CASCADE)
    permitted = models.ForeignKey(User, related_name='authorisations', on_delete=models.DO_NOTHING)
    authority = models.ForeignKey(Authority, related_name='authorisations', on_delete=models.DO_NOTHING)
    
    @classmethod
    def create(cls, matrix, permitted, authority):
        return cls(matrix=matrix, permitted=permitted, authority=authority)
    
    def __str__(self):
        return f"{self.id}, {self.matrix.id}, {self.permitted.id}, {self.authority.id}"

    def __repr__(self):
        return f"{self.id}, {self.matrix.id}, {self.permitted.id}, {self.authority.id}"


    def set_matrix(self, a_matrix):
        self.matrix = a_matrix

    def is_permitted_by(self, a_user):
        if self.permitted == a_user:
            return True
        else:
            return False
            
    def set_permitted(self, a_user):
        self.permitted = a_user
        
    def is_authority(self, a_authority):
        if self.authority == a_authority:
            return True
        else:
            return False
            
    def set_authority(self, a_authority):
        self.authority = a_authority
        
    def has_authority(self, a_matrix, a_user):
        if self.permitted == a_user:
            return True
        else:
            return False
            

def authorisation_list_select_related_matrix():

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


def authorisation_list_select_related_matrix_by_user(a_user):

	queryset = Authorisation.objects.select_related('matrix').filter(permitted=a_user)
	
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


def matrix_list_by_user(a_user):

	queryset = Matrix.objects.filter(owner=a_user).order_by('id')
	
	matrices = list()
	
	for matrix in queryset:
	
		out_matrix = ({
        	'matrix_id': matrix.id, 
	        'matrix_title': matrix.title, 
   		    'matrix_description': matrix.description, 
        	'matrix_blogpost': matrix.blogpost, 
	        'matrix_created': matrix.created, 
   		    'matrix_modified': matrix.modified, 
       		'matrix_height': matrix.height, 
	        'matrix_width': matrix.width, 
   		    'matrix_owner': matrix.owner.username,
    	    'authorisation_id': "0", 
    	    'authorisation_authority': "OWNER",
    	    'authorisation_permitted': matrix.owner.username
		})

		matrices.append(out_matrix)
    
	return matrices


def matrix_list_not_by_user(a_user):

	queryset = Matrix.objects.filter(~Q(owner=a_user)).order_by('id')
	
	matrices = list()
	
	for matrix in queryset:
	
		out_matrix = ({
        	'matrix_id': matrix.id, 
	        'matrix_title': matrix.title, 
   		    'matrix_description': matrix.description, 
        	'matrix_blogpost': matrix.blogpost, 
	        'matrix_created': matrix.created, 
   		    'matrix_modified': matrix.modified, 
       		'matrix_height': matrix.height, 
	        'matrix_width': matrix.width, 
   		    'matrix_owner': matrix.owner.username,
    	    'authorisation_id': "0", 
    	    'authorisation_authority': "ADMIN",
    	    'authorisation_permitted': matrix.owner.username
		})


		matrices.append(out_matrix)
    
	return matrices


def matrix_list_all():

	queryset = Matrix.objects.all().order_by('id')
	
	matrices = list()
	
	for matrix in queryset:
	
		out_matrix = ({
        	'matrix_id': matrix.id, 
	        'matrix_title': matrix.title, 
   		    'matrix_description': matrix.description, 
        	'matrix_blogpost': matrix.blogpost, 
	        'matrix_created': matrix.created, 
   		    'matrix_modified': matrix.modified, 
       		'matrix_height': matrix.height, 
	        'matrix_width': matrix.width, 
   		    'matrix_owner': matrix.owner.username,
    	    'authorisation_id': "0", 
   	    	'authorisation_authority': "ADMIN",
       		'authorisation_permitted': matrix.owner.username
        	})

		matrices.append(out_matrix)
    
	return matrices


def get_authority_for_matrix_and_user_and_requester(a_matrix, a_user):

	authority = Authority.create("NONE", a_user)

	if a_user.is_superuser == True:
		authority.set_as_admin()

	else:

		if a_user == a_matrix.owner:
			authority.set_as_owner()

		else:
	
			if Authorisation.objects.filter(Q(matrix=a_matrix) & Q(permitted=a_user)).exists():
		
				authorisation = Authorisation.objects.get(Q(matrix=a_matrix) & Q(permitted=a_user))
				
				if authorisation.authority.is_owner() == True:
					authority.set_as_owner()

				if authorisation.authority.is_admin() == True:
					authority.set_as_admin()

				if authorisation.authority.is_viewer() == True:
					authority.set_as_viewer()

				if authorisation.authority.is_editor() == True:
					authority.set_as_editor()
			
			else:
				authority.set_as_none()

	return authority


def credential_exists(a_user):

	return Credential.objects.filter(username=a_user.username).values('username').exists()


def credential_apppwd(a_user):

	return Credential.objects.filter(username=a_user.username).values('apppwd')


def authorisation_exits_for_matrix_and_permitted(a_matrix, a_user):

	return Authorisation.objects.filter(matrix=a_matrix).filter(permitted=a_user).exists()


def get_primary_wordpress_server():

	return Server.objects.get(url_server=config('WORDPRESS'))

