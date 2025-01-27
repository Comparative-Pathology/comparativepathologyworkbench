#!/usr/bin/python3
#
# ##
# \file         server.py
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
# The (image) Server Model.
# ##
#
from __future__ import unicode_literals

import requests
import base64
import omero

from django.db import models
from django.contrib.auth.models import User
from django.apps import apps

from omero.gateway import BlitzGateway

from random import randint

from decouple import config

from matrices.routines import AESCipher

from matrices.models import Type


CMD_API_WORDPRESS_IMAGE = 'WordpressImage'
CMD_API_WORDPRESS_IMAGES = 'WordpressImages'
CMD_API_IMAGES = 'Images'
CMD_API_IMAGE_DATASETS = 'ImageDatasets'
CMD_API_API = 'API'
CMD_API_TOKEN = 'Token'
CMD_API_LOGIN = 'Login'
CMD_API_GROUP_DATASETS = 'GroupDatasets'
CMD_API_GROUP_IMAGES = 'GroupImages'
CMD_API_PROJECTS = 'Projects'
CMD_API_GROUP_PROJECTS = 'GroupProjects'
CMD_API_REGION = 'Region'
CMD_API_THUMBNAIL = 'Thumbnail'
CMD_API_VIEWER = 'Viewer'
CMD_API_BIRDS_EYE = 'BirdsEye'
CMD_API_DATASET = 'Dataset'
CMD_API_DATASET_IMAGES = 'DatasetImages'
CMD_API_DATASET_PROJECTS = 'DatasetProjects'
CMD_API_IMAGE_ROIS = 'ImageROIs'
CMD_API_PROJECT_DATASETS = 'ProjectDatasets'
CMD_API_PUBLIC_VIEWER = 'PublicViewer'

SERVER_WORDPRESS = 'WORDPRESS'
SERVER_OMERO_547 = 'OMERO_5.4.7'
SERVER_EBI_SCA = 'EBI_SCA'
SERVER_CPW = 'CPW'
SERVER_IDR = 'idr.openmicroscopy.org'


#
#    The Server Manager Class
#
class ServerManager(models.Manager):

    def get_or_none(self, *args, **kwargs):

        try:

            return self.get(*args, **kwargs)

        except (KeyError, Server.DoesNotExist):

            return None


#
#   Class SERVER
#
class Server(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    url_server = models.CharField(max_length=50, blank=False, default='')
    uid = models.CharField(max_length=50, blank=True, default='')
    pwd = models.CharField(max_length=50, blank=True, default='')
    type = models.ForeignKey(Type, related_name='servers', default=0, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='servers', on_delete=models.DO_NOTHING)
    accessible = models.BooleanField(default=False)

    objects = ServerManager()

    @classmethod
    def create(cls, name, url_server, uid, pwd, type, owner, accessible):
        return cls(name=name, url_server=url_server, uid=uid, pwd=pwd, type=type, owner=owner, accessible=accessible)

    def __str__(self):
        return f"{self.uid}@{self.url_server}"

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.url_server}, {self.uid}, {self.pwd}, {self.type.id}, {self.owner.id}, \
        {self.accessible}"

    def is_owned_by(self, a_user):
        if self.owner == a_user:
            return True
        else:
            return False

    def set_owner(self, a_user):
        self.owner = a_user

    def set_pwd(self, a_pwd):
        self.pwd = a_pwd

    def set_accessible(self):
        self.accessible = True

    def set_inaccessible(self):
        self.accessible = False

    def is_accessible(self):
        if self.accessible is True:
            return True
        else:
            return False

    def is_not_accessible(self):
        if self.accessible is False:
            return True
        else:
            return False

    def is_wordpress(self):
        if self.type.name == SERVER_WORDPRESS:
            return True
        else:
            return False

    def is_omero547(self):
        if self.type.name == SERVER_OMERO_547:
            return True
        else:
            return False

    def is_ebi_sca(self):
        if self.type.name == SERVER_EBI_SCA:
            return True
        else:
            return False

    def is_cpw(self):
        if self.type.name == SERVER_CPW:
            return True
        else:
            return False

    def is_idr(self):
        if self.url_server == SERVER_IDR:
            return True
        else:
            return False

    def get_uid_and_url(self):
        return f"{self.uid}@{self.url_server}"

    #
    #   WORDPRESS INTERFACE
    #
    #
    #   Get the JSON Details for the Requested Server
    #
    def get_wordpress_json(self, credential, page_id):

        Command = apps.get_model('matrices', 'Command')

        commandWordpressImages = Command.objects.filter(type=self.type).get(name=CMD_API_WORDPRESS_IMAGES)

        images_url = commandWordpressImages.protocol.name + '://' + self.url_server + '/' + \
            commandWordpressImages.application + '/' + commandWordpressImages.preamble + str(page_id) + \
            commandWordpressImages.postamble + str(credential.wordpress)

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
                    'imageCount': image_total,
                    'prev_page': prev_page,
                    'next_page': next_page
                })

                data = {
                    'server': self,
                    'group': group,
                    'projects': project_list,
                    'dataset': dataset,
                    'images': images_list
                }

            else:

                group = ''
                project_list = []

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

                data = {
                    'server': self,
                    'group': group,
                    'projects': project_list,
                    'dataset': dataset
                }

        except Exception as e:

            print("Exception e : " + str(e))

            group = ''
            project_list = []

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

            data = {
                'server': self,
                'group': group,
                'projects': project_list,
                'dataset': dataset
            }

        return data

    #
    #   Get the JSON Details for the Requested Image
    #
    def get_wordpress_image_json(self, credential, image_id):

        Command = apps.get_model('matrices', 'Command')

        commandWordpressImage = Command.objects.filter(type=self.type).get(name=CMD_API_WORDPRESS_IMAGE)

        image_url = commandWordpressImage.protocol.name + '://' + self.url_server + '/' + \
            commandWordpressImage.application + '/' + commandWordpressImage.preamble + '/' + str(image_id)

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

                group = ''
                project_list = []
                datasets = []
                projects = []

                data = {
                    'server': self,
                    'group': group,
                    'projects': projects,
                    'datasets': datasets,
                    'image': image
                }

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

                group = ''
                project_list = []
                datasets = []
                projects = []

                data = {
                    'server': self,
                    'group': group,
                    'projects': projects,
                    'datasets': datasets,
                    'image': image
                }

        except Exception as e:

            print("Exception e : " + str(e))

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
            datasets = []
            projects = []

            data = {
                'server': self,
                'group': group,
                'projects': projects,
                'datasets': datasets,
                'image': image
            }

        return data

    #
    #   EBI INTERFACE
    #
    #
    #   Get the JSON Details for the Requested Server
    #
    def get_ebi_server_experiment_metadata(self, an_experiment_id):

        experiments_url = 'json/experiments'

        full_experiments_url = 'https://' + self.url_server + '/' + experiments_url + '/'

        session = requests.Session()
        session.timeout = 10

        payload = {'limit': 100}

        try:
            data = session.get(full_experiments_url, params=payload).json()

        except Exception as e:

            print("Exception e : " + str(e))

            experiment_metadata = ({
                'experimentType': 'ERROR',
                'experimentAccession': 'ERROR',
                'experimentDescription': 'ERROR',
                'loadDate': 'ERROR',
                'lastUpdate': 'ERROR',
                'numberOfAssays': 'ERROR',
                'numberOfContrasts': 'ERROR',
                'species': 'ERROR',
                'kingdom': 'ERROR',
                'technologyType': 'ERROR',
                'experimentalFactors': 'ERROR',
                'experimentProject': 'ERROR'
            })

            return experiment_metadata

        assert len(data['experiments']) < 1000

        experiment_metadata = ()

        for p in data['experiments']:

            if an_experiment_id == p['experimentAccession']:

                technologyType = ''
                experimentalFactors = ''
                experimentProject = ''

                if 'technologyType' in p:

                    for a in p['technologyType']:

                        if technologyType == '':

                            technologyType = a

                        else:

                            technologyType = technologyType + ', ' + a

                if 'experimentalFactors' in p:

                    for b in p['experimentalFactors']:

                        if experimentalFactors == '':

                            experimentalFactors = b

                        else:

                            experimentalFactors = experimentalFactors + ', ' + b

                if 'experimentProject' in p:

                    for c in p['experimentProject']:

                        if experimentProject == '':

                            experimentProject = c

                        else:

                            experimentProject = experimentProject + ', ' + c

                experiment_metadata = ({
                    'experimentType': p['experimentType'],
                    'experimentAccession': p['experimentAccession'],
                    'experimentDescription': p['experimentDescription'],
                    'loadDate': p['loadDate'],
                    'lastUpdate': p['lastUpdate'],
                    'numberOfAssays': p['numberOfAssays'],
                    'numberOfContrasts': '',
                    'species': p['species'],
                    'kingdom': p['kingdom'],
                    'technologyType': technologyType,
                    'experimentalFactors': experimentalFactors,
                    'experimentProject': experimentProject
                })

        return experiment_metadata

    #
    #   Get the JSON Details for the Requested Server
    #
    def get_ebi_server_json(self):

        experiments_url = 'json/experiments'

        full_experiments_url = 'https://' + self.url_server + '/' + experiments_url + '/'

        session = requests.Session()
        session.timeout = 10

        payload = {'limit': 100}
        data = session.get(full_experiments_url, params=payload).json()
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

        data = {
            'server': self,
            'experiment_list': experiment_list
        }

        return data

    #
    #   Get the JSON Details for the Requested Server
    #
    def get_ebi_widget_json(self):

        data = {
            'server': self
        }

        return data

    #
    #   OMERO INTERFACE
    #
    #
    #   Get the JSON Details for the Requested Server
    #
    def get_imaging_server_json(self):

        Command = apps.get_model('matrices', 'Command')

        commandAPI = Command.objects.filter(type=self.type).get(name=CMD_API_API)
        commandToken = Command.objects.filter(type=self.type).get(name=CMD_API_TOKEN)
        commandLogin = Command.objects.filter(type=self.type).get(name=CMD_API_LOGIN)
        commandProjects = Command.objects.filter(type=self.type).get(name=CMD_API_PROJECTS)
        commandGroupProjects = Command.objects.filter(type=self.type).get(name=CMD_API_GROUP_PROJECTS)
        commandGroupDatasets = Command.objects.filter(type=self.type).get(name=CMD_API_GROUP_DATASETS)
        commandDatasetImages = Command.objects.filter(type=self.type).get(name=CMD_API_DATASET_IMAGES)

        commandBirdsEye = Command.objects.filter(type=self.type).get(name=CMD_API_BIRDS_EYE)

        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application

        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'

        projects_url = commandProjects.protocol.name + '://' + self.url_server + '/' + commandProjects.application + \
            '/' + commandProjects.preamble
        group_projects_url = commandGroupProjects.protocol.name + '://' + self.url_server + '/' + \
            commandGroupProjects.application + '/' + commandGroupProjects.preamble
        datasets_url = commandGroupDatasets.protocol.name + '://' + self.url_server + '/' + \
            commandGroupDatasets.application + '/' + commandGroupDatasets.preamble
        dataset_images_url = commandDatasetImages.protocol.name + '://' + self.url_server + '/' + \
            commandDatasetImages.application + '/' + commandDatasetImages.preamble

        session = requests.Session()
        session.timeout = 10

        if self.id == 33:

            session.verify = False

        else:

            session.verify = True

        try:
            r = session.get(api_url)

        except Exception as e:

            print("Exception e : " + str(e))

            group_count = 0
            group_list = []

            data = {
                'server': self,
                'group_list': group_list,
                'group_count': group_count
            }

            return data

        token = session.get(token_url).json()['data']
        session.headers.update({'X-CSRFToken': token, 'Referer': login_url})

        userid = self.uid

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        password = cipher.decrypt(self.pwd)

        memberOfGroup_list = list()

        group_list = list()

        group_count = 0

        if userid == "":

            project_url = projects_url + '/' + commandProjects.postamble

            payload = {'limit': 100}
            project_rsp = session.get(project_url, params=payload)
            project_data = project_rsp.json()

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

                group_count = 0
                group_list = []

                data = {
                    'server': self,
                    'group_list': group_list,
                    'group_count': group_count
                }

                return data

            eventContext = login_rsp['eventContext']
            memberOfGroups = eventContext['memberOfGroups']

            memberOfGroup_list = memberOfGroups

        for mog in memberOfGroup_list:

            group_project_url = group_projects_url + str(mog)
            dataset_url = datasets_url + str(mog) + commandGroupDatasets.postamble

            payload = {'limit': 100}
            group_project_rsp = session.get(group_project_url, params=payload)
            group_project_data = group_project_rsp.json()

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

                    payload = {'limit': 300}
                    dataset_rsp = session.get(dataset_url, params=payload)
                    dataset_data = dataset_rsp.json()

                    datasetCount = ''

                    randImageID = ''
                    randImageName = ''
                    randomImageBEURL = ''

                    if dataset_rsp.status_code == 200:

                        imageCount = 0

                        dataset_meta = dataset_data['meta']
                        datasetCount = dataset_meta['totalCount']

                        if userid == "":

                            randImageID = '999999'
                            randImageName = 'NONE'
                            randomImageBEURL = 'NONE'

                        else:

                            randImageID = '999999'
                            randImageName = 'NONE'
                            randomImageBEURL = 'NONE'

                            for d in dataset_data['data']:

                                if randImageID == '999999' and randImageName == 'NONE' and randomImageBEURL == 'NONE':

                                    datasetId = d['@id']

                                    dataset_image_url = dataset_images_url + '/' + str(datasetId) + '/' + \
                                        commandDatasetImages.postamble

                                    payload = {'limit': 300}
                                    dataset_image_rsp = session.get(dataset_image_url, params=payload)
                                    dataset_image_data = dataset_image_rsp.json()

                                    if dataset_image_rsp.status_code == 200:

                                        dataset_image_meta = dataset_image_data['meta']
                                        imageCount = dataset_image_meta['totalCount']

                                        groupImageCount = groupImageCount + imageCount

                                        if imageCount > 0:

                                            randImageIndex = randint(0, (imageCount - 1))

                                            count = 0

                                            for i in dataset_image_data['data']:

                                                if count == randImageIndex:
                                                    randImageID = i['@id']
                                                    randImageName = i['Name']
                                                    break

                                                count = count + 1

                                        randomImageBEURL = commandBirdsEye.protocol.name + '://' + self.url_server + \
                                            '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + \
                                            str(randImageID) + '/' + commandBirdsEye.postamble

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

        data = {
            'server': self,
            'group_list': new_group_list,
            'group_count': group_count
        }

        return data

    #
    #   Get the JSON Details for the Requested Server via the Blitz Gateway
    #
    def get_imaging_server_json_blitz(self, gateway_port):

        conn = None

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        byte_password = cipher.decrypt(self.pwd)
        password = byte_password.decode('utf-8')

        conn = BlitzGateway(self.uid, password, host=self.url_server, port=gateway_port, secure=True)
        conn.connect()

        groupCount = 0

        group_list = list()

        group = conn.getGroupFromContext()
        group_ctx_id = str(group.getId())

        for group_ome in conn.getGroupsMemberOf():

            group_ome_id = str(group_ome.getId())
            group_ome_name = str(group_ome.getName())

            if group_ctx_id == group_ome_id:

                projectCount = 0

                projects = conn.getObjects("Project", opts={'group': group_ome_id})

                projectCount = len(list(projects))

                datasetCount = 0

                for project_ome in conn.getObjects("Project", opts={'group': group_ome_id}):

                    datasets = project_ome.listChildren()

                    thisDatasetCount = len(list(datasets))

                    datasetCount = datasetCount + thisDatasetCount

                group = ({
                    'id': group_ome_id,
                    'name': group_ome_name,
                    'projectCount': projectCount,
                    'datasetCount': datasetCount
                })

                groupCount = groupCount + 1

                group_list.append(group)

        conn.close()

        data = {
            'server': self,
            'group_list': group_list,
            'group_count': groupCount
        }

        return data

    #
    #   Get the JSON Details for the Requested Group
    #
    def get_imaging_server_group_json(self, group_id):

        Command = apps.get_model('matrices', 'Command')

        commandAPI = Command.objects.filter(type=self.type).get(name=CMD_API_API)
        commandToken = Command.objects.filter(type=self.type).get(name=CMD_API_TOKEN)
        commandLogin = Command.objects.filter(type=self.type).get(name=CMD_API_LOGIN)

        commandGroupProjects = Command.objects.filter(type=self.type).get(name=CMD_API_GROUP_PROJECTS)
        commandProjectsDatasets = Command.objects.filter(type=self.type).get(name=CMD_API_PROJECT_DATASETS)

        commandDatasetImages = Command.objects.filter(type=self.type).get(name=CMD_API_DATASET_IMAGES)
        commandBirdsEye = Command.objects.filter(type=self.type).get(name=CMD_API_BIRDS_EYE)

        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'

        groups_url = commandGroupProjects.protocol.name + '://' + self.url_server + '/' + \
            commandGroupProjects.application + '/' + commandGroupProjects.preamble
        datasets_url = commandProjectsDatasets.protocol.name + '://' + self.url_server + '/' + \
            commandProjectsDatasets.application + '/' + commandProjectsDatasets.preamble + '/'

        images_url = commandDatasetImages.protocol.name + '://' + self.url_server + '/' + \
            commandDatasetImages.application + '/' + commandDatasetImages.preamble + '/'

        session = requests.Session()

        if self.id == 33:

            session.verify = False

        else:

            session.verify = True

        try:
            r = session.get(api_url)

        except Exception as e:

            print("Exception e : " + str(e))

            group_list = []

            data = {
                'server': self,
                'project_list': project_list,
                'group': group
            }

            return data

        token = session.get(token_url).json()['data']
        session.headers.update({'X-CSRFToken': token, 'Referer': login_url})

        userid = self.uid

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        password = cipher.decrypt(self.pwd)

        memberOfGroup_list = list()

        group_list = list()

        if userid == "":

            project_url = groups_url + str(group_id) + commandGroupProjects.postamble

            payload = {'limit': 100}
            project_rsp = session.get(project_url, params=payload)
            project_data = project_rsp.json()

            if project_rsp.status_code == 200:

                project_meta = project_data['meta']
                projectCount = project_meta['totalCount']

                for p in project_data['data']:

                    details = p['omero:details']

                    groupdetails = details['group']

                    groupId = groupdetails['@id']

                    if groupId == group_id:

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

                group_list = []

                data = {
                    'server': self,
                    'project_list': project_list,
                    'group': group
                }

                return data

            eventContext = login_rsp['eventContext']
            memberOfGroups = eventContext['memberOfGroups']

            memberOfGroup_list = memberOfGroups

        project_list = list()
        group_list = list()
        group = ''

        for mog in memberOfGroup_list:

            if mog == group_id:

                project_url = groups_url + str(group_id) + commandGroupProjects.postamble

                payload = {'limit': 300}
                project_data = session.get(project_url, params=payload).json()

                assert len(project_data['data']) < 2000

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

                    group_list.append(group)

                    project_id = p['@id']
                    projectName = p['Name']

                    dataset_url = datasets_url + str(project_id) + '/' + commandProjectsDatasets.postamble

                    payload = {'limit': 500}
                    dataset_rsp = session.get(dataset_url, params=payload)
                    dataset_data = dataset_rsp.json()

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

                                randImageIndex = 0

                                count = 0

                                if datasetCount == 1:

                                    payload = {'limit': 500}
                                    image_data = session.get(image_url, params=payload).json()

                                    assert len(dataset_data['data']) < 1000

                                    for i in image_data['data']:

                                        if count == randImageIndex:
                                            randImageID = i['@id']
                                            randImageName = i['Name']

                                        count = count + 1

                                    randomImageBEURL = commandBirdsEye.protocol.name + '://' + self.url_server \
                                        + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + \
                                        str(randImageID) + '/' + commandBirdsEye.postamble

                    project = ({
                        'id': project_id,
                        'name': projectName,
                        'datasetCount': datasetCount,
                        'imageCount': imageCount,
                        'randomImageID': randImageID,
                        'randomImageName': randImageName,
                        'randomImageBEURL': randomImageBEURL
                    })

                    project_list.append(project)

        project_count = 0

        for project in project_list:

            project_count = project_count + 1

        if group_list == []:

            group = ({
                'id': group_id,
                'name': "ERROR",
                'projectCount': 0
            })

        else:

            group = group_list[0]

        data = {
            'server': self,
            'project_count': project_count,
            'project_list': project_list,
            'group': group
        }

        return data

    #
    #   Get the JSON Details for the Requested Group via the Blitz Gateway
    #
    def get_imaging_server_group_json_blitz(self, group_id, gateway_port):

        Command = apps.get_model('matrices', 'Command')

        commandBirdsEye = Command.objects.filter(type=self.type).get(name=CMD_API_BIRDS_EYE)

        conn = None

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        byte_password = cipher.decrypt(self.pwd)
        password = byte_password.decode('utf-8')

        conn = BlitzGateway(self.uid, password, host=self.url_server, port=gateway_port, secure=True)
        conn.connect()

        project_list = list()

        group_ome_id = ''
        group_ome_name = ''

        for g in conn.getGroupsMemberOf():

            if g.getId() == group_id:

                group_ome_id = g.getId()
                group_ome_name = g.getName()

        group = ({
            'id': group_ome_id,
            'name': group_ome_name
        })

        projectCount = 0

        for project_ome in conn.getObjects("Project", opts={'group': group_id}):

            imageCount = 0
            datasetCount = 0

            projectCount = projectCount + 1

            project_ome_id = project_ome.getId()
            project_ome_name = project_ome.getName()

            for dataset_ome in project_ome.listChildren():

                datasetCount = datasetCount + 1

                randImageIndex = 0

                for image_ome in dataset_ome.listChildren():

                    if imageCount == randImageIndex:

                        randImageID = str(image_ome.getId())
                        randImageName = str(image_ome.getName())

                        randomImageBEURL = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + \
                            commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(randImageID) + \
                            '/' + commandBirdsEye.postamble

                    imageCount = imageCount + 1

            project = ({
                'id': project_ome_id,
                'name': project_ome_name,
                'datasetCount': datasetCount,
                'imageCount': imageCount,
                'randomImageID': randImageID,
                'randomImageName': randImageName,
                'randomImageBEURL': randomImageBEURL
            })

            project_list.append(project)

        conn.close()

        data = {
            'server': self,
            'project_count': projectCount,
            'project_list': project_list,
            'group': group
        }

        return data

    #
    #   Get the JSON Details for the Requested Project
    #
    def get_imaging_server_project_json(self, project_id, page_id, pagination_amt):

        Command = apps.get_model('matrices', 'Command')

        commandAPI = Command.objects.filter(type=self.type).get(name=CMD_API_API)
        commandToken = Command.objects.filter(type=self.type).get(name=CMD_API_TOKEN)
        commandLogin = Command.objects.filter(type=self.type).get(name=CMD_API_LOGIN)

        commandProjects = Command.objects.filter(type=self.type).get(name=CMD_API_PROJECTS)
        commandProjectsDatasets = Command.objects.filter(type=self.type).get(name=CMD_API_PROJECT_DATASETS)

        commandDatasetImages = Command.objects.filter(type=self.type).get(name=CMD_API_DATASET_IMAGES)
        commandBirdsEye = Command.objects.filter(type=self.type).get(name=CMD_API_BIRDS_EYE)

        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'

        projects_url = commandProjects.protocol.name + '://' + self.url_server + '/' + commandProjects.application + \
            '/' + commandProjects.preamble + '/'

        images_url = commandDatasetImages.protocol.name + '://' + self.url_server + '/' + \
            commandDatasetImages.application + '/' + commandDatasetImages.preamble + '/'

        session = requests.Session()

        if self.id == 33:

            session.verify = False

        else:

            session.verify = True

        try:
            r = session.get(api_url)

        except Exception as e:

            print("Exception e : " + str(e))

            group = ''
            project = ''
            dataset_list = []

            data = {
                'server': self,
                'group': group,
                'project': project,
                'dataset_list': dataset_list
            }

            return data

        token = session.get(token_url).json()['data']
        session.headers.update({'X-CSRFToken': token, 'Referer': login_url})

        userid = self.uid

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        password = cipher.decrypt(self.pwd)

        if userid != "":

            payload = {'username': userid, 'password': password, 'server': 1}

            r = session.post(login_url, data=payload)
            login_rsp = r.json()
            assert r.status_code == 200
            assert login_rsp['success']

        limit_str = '&limit=' + str(pagination_amt)
        offset = pagination_amt * (int(page_id) - 1)
        offset_str = '&offset=' + str(offset)

        project_url = projects_url + str(project_id) + '/' + commandProjects.postamble + limit_str + offset_str
        dataset_url = projects_url + str(project_id) + '/' + commandProjectsDatasets.postamble + limit_str + offset_str

        dataset_list = list()

        datasets_data = session.get(dataset_url).json()
        assert len(datasets_data['data']) < 1000

        project_data = session.get(project_url).json()

        if 'message' in project_data:

            message = project_data['message']

            group = ({
                'id': 0,
                'name': '',
            })

            project = ({
                'id': project_id,
                'name': "ERROR",
                'datasetCount': 0,
            })

        else:

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

            randImageID = ''
            randImageName = ''
            randomImageBEURL = ''

            ddata = datasets_data['data']

            dataset_count = 0

            for d in ddata:

                dataset_id = d['@id']
                datasetName = d['Name']
                imageCount = d['omero:childCount']

                randImageID = ''
                randImageName = ''
                randomImageBEURL = ''

                image_url = images_url + str(dataset_id) + '/' + commandDatasetImages.postamble

                randImageIndex = 0
                count = 0

                payload = {'limit': 300}
                image_data = session.get(image_url, params=payload).json()
                assert len(image_data['data']) < 2000

                for i in image_data['data']:

                    if count == randImageIndex:
                        randImageID = i['@id']
                        randImageName = i['Name']

                    count = count + 1

                randomImageBEURL = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + \
                    commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + \
                    str(randImageID) + '/' + commandBirdsEye.postamble

                dataset = ({
                    'id': dataset_id,
                    'name': datasetName,
                    'imageCount': imageCount,
                    'randomImageID': randImageID,
                    'randomImageName': randImageName,
                    'randomImageBEURL': randomImageBEURL
                })

                dataset_count = dataset_count + 1

                dataset_list.append(dataset)

        prev_page = '1'
        next_page = '1'

        page_count = int(page_id) * pagination_amt

        dataset_total = ((int(page_id) - 1) * pagination_amt) + dataset_count

        if dataset_count < pagination_amt:

            next_page = '1'

        if dataset_total % pagination_amt == 0:

            next_page = int(page_id) + 1

        else:

            next_page = '1'

        if int(page_id) == 1:

            prev_page = page_id

        else:

            prev_page = int(page_id) - 1

        dataset_start = offset + 1
        dataset_end = offset + pagination_amt

        if dataset_end > dataset_total:

            dataset_end = dataset_total

        data = {
            'server': self,
            'group': group,
            'project': project,
            'dataset_list': dataset_list,
            'prev_page': str(prev_page),
            'next_page': str(next_page),
            'dataset_start': dataset_start,
            'dataset_end': dataset_end
        }

        return data

    #
    #   Get the JSON Details for the Requested Project via Blitz Gateway
    #
    def get_imaging_server_project_json_blitz(self, project_id, page_id, pagination_amt, gateway_port):

        Command = apps.get_model('matrices', 'Command')

        commandBirdsEye = Command.objects.filter(type=self.type).get(name=CMD_API_BIRDS_EYE)

        dataset_list = list()

        dataset_count = 0

        conn = None

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        byte_password = cipher.decrypt(self.pwd)
        password = byte_password.decode('utf-8')

        conn = BlitzGateway(self.uid, password, host=self.url_server, port=gateway_port, secure=True)
        conn.connect()

        limit_str = str(pagination_amt)
        offset = pagination_amt * (int(page_id) - 1)
        offset_str = str(offset)

        project_ome = conn.getObject("Project", str(project_id))

        if project_ome is None:

            group = ({
                'id': '',
                'name': ''
            })

            project = ({
                'id': project_id,
                'name': "ERROR",
                'datasetCount': 0,
            })

        else:

            group = ({
                'id': str(conn.getEventContext().groupId),
                'name': str(conn.getEventContext().groupName)
            })

            datasets_ome = project_ome.listChildren()

            datasets_ome_count = 0

            for dataset_ome in datasets_ome:

                datasets_ome_count = datasets_ome_count + 1

            datasets_ome = conn.getObjects("Dataset", opts={'project': str(project_id),
                                                            'order_by': 'lower(obj.name)',
                                                            'limit': limit_str,
                                                            'offset': offset_str})

            for dataset_ome in datasets_ome:

                dataset_id = dataset_ome.getId()
                datasetName = dataset_ome.getName()

                randImageIndex = 0
                imageCount = 0

                for image_ome in dataset_ome.listChildren():

                    if imageCount == randImageIndex:

                        randImageID = str(image_ome.getId())
                        randImageName = str(image_ome.getName())

                    imageCount = imageCount + 1

                randomImageBEURL = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + \
                    commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(randImageID) + \
                    '/' + commandBirdsEye.postamble

                dataset = ({
                    'id': dataset_id,
                    'name': datasetName,
                    'imageCount': str(imageCount),
                    'randomImageID': randImageID,
                    'randomImageName': randImageName,
                    'randomImageBEURL': randomImageBEURL
                })

                dataset_count = dataset_count + 1

                dataset_list.append(dataset)

            project = ({
                'id': project_ome.getId(),
                'name': project_ome.getName(),
                'datasetCount': str(datasets_ome_count)
            })

        conn.close()

        prev_page = '1'
        next_page = '1'

        page_count = int(page_id) * pagination_amt

        dataset_total = ((int(page_id) - 1) * pagination_amt) + dataset_count

        if dataset_count < pagination_amt:

            next_page = '1'

        if dataset_total % pagination_amt == 0:

            next_page = int(page_id) + 1

        else:

            next_page = '1'

        if int(page_id) == 1:

            prev_page = page_id

        else:

            prev_page = int(page_id) - 1

        dataset_start = offset + 1
        dataset_end = offset + pagination_amt

        if dataset_end > dataset_total:

            dataset_end = dataset_total

        data = {
            'server': self,
            'group': group,
            'project': project,
            'dataset_list': dataset_list,
            'prev_page': str(prev_page),
            'next_page': str(next_page),
            'dataset_start': dataset_start,
            'dataset_end': dataset_end
        }

        return data

    #
    #   Get the JSON Details for the Requested Dataset
    #
    def get_imaging_server_dataset_json(self, dataset_id, filter):

        Command = apps.get_model('matrices', 'Command')

        userid = self.uid

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        password = cipher.decrypt(self.pwd)

        if userid == "":

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_PUBLIC_VIEWER)

        else:

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_VIEWER)

        commandAPI = Command.objects.filter(type=self.type).get(name=CMD_API_API)
        commandToken = Command.objects.filter(type=self.type).get(name=CMD_API_TOKEN)
        commandLogin = Command.objects.filter(type=self.type).get(name=CMD_API_LOGIN)

        commandDataset = Command.objects.filter(type=self.type).get(name=CMD_API_DATASET)
        commandDatasetProjects = Command.objects.filter(type=self.type).get(name=CMD_API_DATASET_PROJECTS)
        commandDatasetImages = Command.objects.filter(type=self.type).get(name=CMD_API_DATASET_IMAGES)

        commandThumbnail = Command.objects.filter(type=self.type).get(name=CMD_API_THUMBNAIL)
        commandBirdsEye = Command.objects.filter(type=self.type).get(name=CMD_API_BIRDS_EYE)

        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'

        datasets_url = commandDataset.protocol.name + '://' + self.url_server + '/' + \
            commandDataset.application + '/' + commandDataset.preamble + '/'
        projects_url = commandDatasetProjects.protocol.name + '://' + self.url_server + '/' + \
            commandDatasetProjects.application + '/' + commandDatasetProjects.preamble + '/'
        images_url = commandDatasetImages.protocol.name + '://' + self.url_server + '/' + \
            commandDatasetImages.application + '/' + commandDatasetImages.preamble + '/'

        session = requests.Session()

        if self.id == 33:

            session.verify = False

        else:

            session.verify = True

        try:
            r = session.get(api_url)

        except Exception as e:

            print("Exception e : " + str(e))

            dataset = ''
            group = ''
            images_list = []
            project_list = []

            data = {
                'server': self,
                'group': group,
                'projects': project_list,
                'images': images_list,
                'dataset': dataset
            }

            return data

        token = session.get(token_url).json()['data']
        session.headers.update({'X-CSRFToken': token, 'Referer': login_url})

        if userid != "":

            payload = {'username': userid, 'password': password, 'server': 1}

            r = session.post(login_url, data=payload)
            login_rsp = r.json()
            assert r.status_code == 200
            assert login_rsp['success']

        dataset_url = datasets_url + str(dataset_id) + '/' + commandDataset.postamble
        projects_url = projects_url + str(dataset_id) + '/' + commandDatasetProjects.postamble
        images_url = datasets_url + str(dataset_id) + '/' + commandDatasetImages.postamble

        project_list = list()
        images_list = list()

        payload = {'limit': 500}
        images_data = session.get(images_url, params=payload).json()

        payload = {'limit': 500}
        dataset_data = session.get(dataset_url, params=payload).json()

        payload = {'limit': 500}
        projects_data = session.get(projects_url, params=payload).json()

        if 'message' in dataset_data:

            message = dataset_data['message']

            group = ({
                'id': 0,
                'name': '',
            })

            project = ({
                'id': 0,
                'name': '',
                'datasetCount': 0,
            })

            dataset = ({
                'id': dataset_id,
                'name': "ERROR",
                'imageCount': 0
            })

        else:

            assert len(images_data['data']) < 2000
            assert len(dataset_data['data']) < 2000
            assert len(projects_data['data']) < 2000

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

            filteredImageCount = 0

            for i in idata:

                image_id = str(i['@id'])
                image_name = i['Name']

                if userid == "":

                    image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                        commandViewer.application + '/' + commandViewer.preamble + '/' + image_id

                else:

                    image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                        commandViewer.application + '/' + commandViewer.preamble + image_id

                image_birdseye_url = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + \
                    commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + image_id + '/' + \
                    commandBirdsEye.postamble

                image_thumbnail_url = commandThumbnail.protocol.name + '://' + self.url_server + '/' + \
                    commandThumbnail.application + '/' + commandThumbnail.preamble + '/' + image_id

                image = ({
                    'id': image_id,
                    'name': image_name,
                    'viewer_url': image_viewer_url,
                    'birdseye_url': image_birdseye_url,
                    'thumbnail_url': image_thumbnail_url
                })

                if filter is True:

                    substring1 = "[macro image]"
                    substring2 = "[macro mask image]"

                    if substring1 not in image_name and substring2 not in image_name:

                        filteredImageCount = filteredImageCount + 1

                        images_list.append(image)

                else:

                    images_list.append(image)

        data = {
            'server': self,
            'group': group,
            'projects': project_list,
            'images': images_list,
            'dataset': dataset,
            'filteredimagecount': filteredImageCount
        }

        return data

    #
    #   Get the JSON Details for the Requested Dataset via the Blitz Gateway
    #
    def get_imaging_server_dataset_json_blitz(self, dataset_id, filter, gateway_port):

        Command = apps.get_model('matrices', 'Command')

        userid = self.uid

        if userid == "":

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_PUBLIC_VIEWER)

        else:

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_VIEWER)

        commandThumbnail = Command.objects.filter(type=self.type).get(name=CMD_API_THUMBNAIL)
        commandBirdsEye = Command.objects.filter(type=self.type).get(name=CMD_API_BIRDS_EYE)

        projects_list = list()
        images_list = list()

        filteredImageCount = 0
        unfilteredImageCount = 0

        conn = None

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        byte_password = cipher.decrypt(self.pwd)
        password = byte_password.decode('utf-8')

        conn = BlitzGateway(self.uid, password, host=self.url_server, port=gateway_port, secure=True)
        conn.connect()

        group = ({
            'id': str(conn.getEventContext().groupId),
            'name': str(conn.getEventContext().groupName)
        })

        dataset_ome = conn.getObject("Dataset", str(dataset_id))

        if dataset_ome is None:

            group = ({
                'id': 0,
                'name': '',
            })

            project = ({
                'id': 0,
                'name': '',
                'datasetCount': 0,
            })

            projects_list.append(project)

            dataset = ({
                'id': dataset_id,
                'name': "ERROR",
                'imageCount': 0
            })

        else:

            project_ome = dataset_ome.getParent()

            project = ({
                'id': project_ome.getId(),
                'name': project_ome.getName()
            })

            projects_list.append(project)

            for image_ome in dataset_ome.listChildren():

                image_id = str(image_ome.getId())
                image_name = str(image_ome.getName())

                if userid == "":

                    image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                        commandViewer.application + '/' + commandViewer.preamble + '/' + image_id

                else:

                    image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                        commandViewer.application + '/' + commandViewer.preamble + image_id

                image_birdseye_url = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + \
                    commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + image_id + '/' + \
                    commandBirdsEye.postamble

                image_thumbnail_url = commandThumbnail.protocol.name + '://' + self.url_server + '/' + \
                    commandThumbnail.application + '/' + commandThumbnail.preamble + '/' + image_id

                image = ({
                    'id': image_id,
                    'name': image_name,
                    'viewer_url': image_viewer_url,
                    'birdseye_url': image_birdseye_url,
                    'thumbnail_url': image_thumbnail_url
                })

                unfilteredImageCount = unfilteredImageCount + 1

                if filter is True:

                    substring1 = "[macro image]"
                    substring2 = "[macro mask image]"

                    if substring1 not in image_name and substring2 not in image_name:

                        filteredImageCount = filteredImageCount + 1

                        images_list.append(image)

                else:

                    images_list.append(image)

            dataset = ({
                'id': dataset_ome.getId(),
                'name': dataset_ome.getName(),
                'imageCount': str(unfilteredImageCount)
            })

        conn.close()

        data = {
            'server': self,
            'group': group,
            'projects': projects_list,
            'images': images_list,
            'dataset': dataset,
            'filteredimagecount': filteredImageCount
        }

        return data

    #
    #   Get the JSON Details for the Requested Image
    #
    def get_imaging_server_image_json(self, image_id):

        Command = apps.get_model('matrices', 'Command')

        userid = self.uid

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        password = cipher.decrypt(self.pwd)

        commandAPI = Command.objects.filter(type=self.type).get(name=CMD_API_API)
        commandToken = Command.objects.filter(type=self.type).get(name=CMD_API_TOKEN)
        commandLogin = Command.objects.filter(type=self.type).get(name=CMD_API_LOGIN)

        commandImages = Command.objects.filter(type=self.type).get(name=CMD_API_IMAGES)
        commandImageDatasets = Command.objects.filter(type=self.type).get(name=CMD_API_IMAGE_DATASETS)
        commandImageROIs = Command.objects.filter(type=self.type).get(name=CMD_API_IMAGE_ROIS)

        commandDatasetProjects = Command.objects.filter(type=self.type).get(name=CMD_API_DATASET_PROJECTS)

        commandViewer = ''

        if userid == "":

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_PUBLIC_VIEWER)

        else:

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_VIEWER)

        commandBirdsEye = Command.objects.filter(type=self.type).get(name=CMD_API_BIRDS_EYE)
        commandRegion = Command.objects.filter(type=self.type).get(name=CMD_API_REGION)

        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'

        images_url = commandImages.protocol.name + '://' + self.url_server + '/' + commandImages.application + \
            '/' + commandImages.preamble + '/'
        datasets_url = commandImageDatasets.protocol.name + '://' + self.url_server + '/' + \
            commandImageDatasets.application + '/' + commandImageDatasets.preamble + '/'
        imagerois_url = commandImageROIs.protocol.name + '://' + self.url_server + '/' + \
            commandImageROIs.application + '/' + commandImageROIs.preamble + '/'

        projects_url = commandDatasetProjects.protocol.name + '://' + self.url_server + '/' + \
            commandDatasetProjects.application + '/' + commandDatasetProjects.preamble + '/'

        if userid == "":

            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                commandViewer.application + '/' + commandViewer.preamble + '/' + str(image_id)

        else:

            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                commandViewer.application + '/' + commandViewer.preamble + str(image_id)

        image_birdseye_url = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + \
            commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(image_id) + '/' + \
            commandBirdsEye.postamble

        image_region_url = commandRegion.protocol.name + '://' + self.url_server + '/' + \
            commandRegion.application + '/' + commandRegion.preamble + '/' + str(image_id) + '/' + \
            commandRegion.postamble

        roi_list = list()
        datasets_list = list()
        projects_list = list()

        session = requests.Session()

        if self.id == 33:

            session.verify = False

        else:

            session.verify = True

        try:

            r = session.get(api_url)

        except Exception as e:

            print("Exception e : " + str(e))

            group_count = 0
            group_list = []

            data = {
                'server': self,
                'group': group,
                'projects': projects_list,
                'datasets': datasets_list,
                'image': image,
                'rois': roi_list
            }

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

        payload = {'limit': 300}
        rois_data = session.get(rois_url, params=payload).json()

        image_url = images_url + str(image_id)

        payload = {'limit': 300}
        image_data = session.get(image_url, params=payload).json()

        if 'message' in image_data:

            group = ({
                'id': 0,
                'name': ''
            })

            image = ({
                'id': image_id,
                'name': "ERROR",
                'description': '',
                'sizeX': 0,
                'sizeY': 0,
                'pixeltype': '',
                'pixelsizeX': 0,
                'pixelsizeY': 0,
                'sizeZ': 0,
                'sizeT': 0,
                'roi_count': 0,
                'viewer_url': '',
                'birdseye_url': ''
            })

        else:

            assert len(rois_data['data']) < 2000

            rmeta = rois_data['meta']
            roiCount = rmeta['totalCount']

            rdata = rois_data['data']

            for r in rdata:

                shapes = r['shapes']
                roi_id = r['@id']

                shape_list = list()

                for s in shapes:
                    shape_id = s['@id']
                    shape_type = s['@type']

                    types = shape_type.split('#')

                    type = types[1]

                    coordX = ''
                    coordY = ''
                    centreX = ''
                    centreY = ''
                    width = '0'
                    height = '0'

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
                        width = str(3192)
                        height = str(3192)

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

                    shape = ({
                        'id': shape_id,
                        'type': type,
                        'shape_url': shape_url,
                        'viewer_url': viewer_url,
                        'x': coordX,
                        'y': coordY,
                        'centre_x': centreX,
                        'centre_y': centreY,
                        'width': width,
                        'height': height
                    })

                    shape_list.append(shape)

                roi = ({
                    'id': roi_id,
                    'shapes': shape_list
                })

                roi_list.append(roi)

            assert len(image_data['data']) < 2000

            data = image_data['data']
            name = data['Name']
            description = data.get('Description', '')
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

            dataset_url = datasets_url + str(image_id) + '/' + commandImageDatasets.postamble

            payload = {'limit': 300}
            dataset_data = session.get(dataset_url, params=payload).json()
            assert len(dataset_data['data']) < 2000

            ddata = dataset_data['data']

            for p in ddata:

                dataset = ({
                    'id': p['@id'],
                    'name': p['Name']
                })

                projects_url = projects_url + str(p['@id']) + '/' + commandDatasetProjects.postamble

                payload = {'limit': 300}
                project_data = session.get(projects_url, params=payload).json()
                assert len(project_data['data']) < 2000

                pdata = project_data['data']

                for p in pdata:

                    project = ({
                        'id': p['@id'],
                        'name': p['Name']
                    })

                    projects_list.append(project)

                datasets_list.append(dataset)

                password = ''

        tag_list = list()

        data = {
            'server': self,
            'group': group,
            'projects': projects_list,
            'datasets': datasets_list,
            'image': image,
            'rois': roi_list,
            'tag_list': tag_list
        }

        return data

    #
    #   Get the JSON Details for the Requested Image via the Blitz Gateway
    #
    def get_imaging_server_image_json_blitz(self, image_id, gateway_port):

        Command = apps.get_model('matrices', 'Command')

        userid = self.uid

        commandViewer = ''
        image_viewer_url = ''

        if userid == "":

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_PUBLIC_VIEWER)

        else:

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_VIEWER)

        if userid == "":

            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                commandViewer.application + '/' + commandViewer.preamble + '/' + str(image_id)

        else:

            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                commandViewer.application + '/' + commandViewer.preamble + str(image_id)

        commandRegion = Command.objects.filter(type=self.type).get(name=CMD_API_REGION)
        commandBirdsEye = Command.objects.filter(type=self.type).get(name=CMD_API_BIRDS_EYE)

        image_region_url = commandRegion.protocol.name + '://' + self.url_server + '/' + \
            commandRegion.application + '/' + commandRegion.preamble + '/' + \
            str(image_id) + '/' + commandRegion.postamble

        image_birdseye_url = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + \
            commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(image_id) + '/' + \
            commandBirdsEye.postamble

        datasets_list = list()
        projects_list = list()
        roi_list = list()
        tag_list = list()

        conn = None

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        byte_password = cipher.decrypt(self.pwd)
        password = byte_password.decode('utf-8')

        conn = BlitzGateway(self.uid, password, host=self.url_server, port=gateway_port, secure=True)
        conn.connect()

        image_ome = conn.getObject("Image", int(image_id))

        if image_ome is None:

            image = ({
                'id': image_id,
                'name': "ERROR",
                'description': '',
                'sizeX': 0,
                'sizeY': 0,
                'pixeltype': '',
                'pixelsizeX': 0,
                'pixelsizeY': 0,
                'sizeZ': 0,
                'sizeT': 0,
                'roi_count': 0,
                'viewer_url': '',
                'birdseye_url': ''
            })

            group = ({
                'id': '',
                'name': ''
            })

            dataset = ({
                'id': '',
                'name': ''
            })

            datasets_list.append(dataset)

            project = ({
                'id': '',
                'name': ''
            })

            projects_list.append(project)

        else:

            image = ({
                'id': image_id,
                'name': str(image_ome.getName()),
                'description': str(image_ome.getDescription()),
                'sizeX': image_ome.getSizeX(),
                'sizeY': image_ome.getSizeY(),
                'pixeltype': '',
                'pixelsizeX': image_ome.getPixelSizeX(),
                'pixelsizeY': image_ome.getPixelSizeY(),
                'sizeZ': image_ome.getSizeZ(),
                'sizeT': image_ome.getSizeT(),
                'roi_count': 0,
                'viewer_url': image_viewer_url,
                'birdseye_url': image_birdseye_url
            })

            group = ({
                'id': image_ome.getDetails().getGroup().getId(),
                'name': image_ome.getDetails().getGroup().getName()
            })

            dataset_ome = image_ome.getParent()

            dataset = ({
                'id': dataset_ome.getId(),
                'name': dataset_ome.getName()
            })

            datasets_list.append(dataset)

            project_ome = dataset_ome.getParent()

            project = ({
                'id': project_ome.getId(),
                'name': project_ome.getName()
            })

            projects_list.append(project)

            for tag in image_ome.listAnnotations():

                tag_list.append(str(tag.getTextValue()))

            roi_service = conn.getRoiService()
            result = roi_service.findByImage(image_ome.getId(), None)

            for roi in result.rois:

                roi_id = roi.getId().getValue()

                shape_list = list()

                for s in roi.copyShapes():

                    shape_id = s.getId().getValue()

                    type = ''
                    coordX = ''
                    coordY = ''
                    centreX = ''
                    centreY = ''
                    width = '0'
                    height = '0'

                    if isinstance(s, omero.model.RectangleI):

                        type = 'Rectangle'

                        centreX = s.getX().getValue()
                        centreY = s.getY().getValue()
                        intCoordX = int(s.getX().getValue())
                        intCoordY = int(s.getY().getValue())
                        intWidth = int(s.getWidth().getValue())
                        intHeight = int(s.getHeight().getValue())

                        coordX = str(intCoordX)
                        coordY = str(intCoordY)
                        width = str(intWidth)
                        height = str(intHeight)

                    elif isinstance(s, omero.model.EllipseI):

                        type = 'Ellipse'

                        centreX = s.getX().getValue()
                        centreY = s.getY().getValue()
                        oldCoordX = s.getX().getValue()
                        oldCoordY = s.getY().getValue()
                        radiusX = s.getRadiusX().getValue()
                        radiusY = s.getRadiusY().getValue()

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

                    elif isinstance(s, omero.model.PointI):

                        type = 'Point'

                        centreX = s.getX().getValue()
                        centreY = s.getY().getValue()
                        intCoordX = int(s.getX().getValue())
                        intCoordY = int(s.getY().getValue())
                        intHalf = 3192 / 2
                        intWidth = intHalf
                        intHeight = intHalf

                        intNewCoordX = intCoordX - intWidth
                        intNewCoordY = intCoordY - intHeight

                        coordX = str(intNewCoordX)
                        coordY = str(intNewCoordY)
                        width = str(3192)
                        height = str(3192)

                    if int(width) > 3192 or int(height) > 3192:

                        middleX = int(coordX) + (int(width)/2)
                        middleY = int(coordY) + (int(height)/2)

                        intX = middleX - (3192/2)
                        intY = middleY - (3192/2)

                        coordX = str(int(intX))
                        coordY = str(int(intY))

                        width = "3192"
                        height = "3192"

                    shape_url = image_region_url + coordX + ',' + coordY + ',' + width + ',' + height
                    viewer_url = image_viewer_url + '&X=' + str(centreX) + '&Y=' + str(centreY) + '&ZM=25'

                    shape = ({
                        'id': shape_id,
                        'type': type,
                        'shape_url': shape_url,
                        'viewer_url': viewer_url,
                        'x': coordX,
                        'y': coordY,
                        'centre_x': centreX,
                        'centre_y': centreY,
                        'width': width,
                        'height': height
                    })

                    shape_list.append(shape)

                roi = ({
                    'id': roi_id,
                    'shapes': shape_list
                })

                roi_list.append(roi)

        conn.close()

        data = {
            'server': self,
            'group': group,
            'projects': projects_list,
            'datasets': datasets_list,
            'image': image,
            'rois': roi_list,
            'tag_list': tag_list
        }

        return data

    #
    #   Get the JSON Details for the Requested Image ROI
    #
    def get_imaging_server_image_roi_json(self, image_id, in_roi):

        Command = apps.get_model('matrices', 'Command')

        userid = self.uid

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        password = cipher.decrypt(self.pwd)

        commandAPI = Command.objects.filter(type=self.type).get(name=CMD_API_API)
        commandToken = Command.objects.filter(type=self.type).get(name=CMD_API_TOKEN)
        commandLogin = Command.objects.filter(type=self.type).get(name=CMD_API_LOGIN)

        commandImages = Command.objects.filter(type=self.type).get(name=CMD_API_IMAGES)
        commandImageDatasets = Command.objects.filter(type=self.type).get(name=CMD_API_IMAGE_DATASETS)
        commandImageROIs = Command.objects.filter(type=self.type).get(name=CMD_API_IMAGE_ROIS)

        commandDatasetProjects = Command.objects.filter(type=self.type).get(name=CMD_API_DATASET_PROJECTS)

        commandViewer = ''

        if userid == "":

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_PUBLIC_VIEWER)

        else:

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_VIEWER)

        commandBirdsEye = Command.objects.filter(type=self.type).get(name=CMD_API_BIRDS_EYE)
        commandRegion = Command.objects.filter(type=self.type).get(name=CMD_API_REGION)

        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'

        images_url = commandImages.protocol.name + '://' + self.url_server + '/' + commandImages.application + \
            '/' + commandImages.preamble + '/'
        datasets_url = commandImageDatasets.protocol.name + '://' + self.url_server + '/' + \
            commandImageDatasets.application + '/' + commandImageDatasets.preamble + '/'
        imagerois_url = commandImageROIs.protocol.name + '://' + self.url_server + '/' + \
            commandImageROIs.application + '/' + commandImageROIs.preamble + '/'

        projects_url = commandDatasetProjects.protocol.name + '://' + self.url_server + '/' + \
            commandDatasetProjects.application + '/' + commandDatasetProjects.preamble + '/'

        if userid == "":

            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                commandViewer.application + '/' + commandViewer.preamble + '/' + str(image_id)

        else:

            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                commandViewer.application + '/' + commandViewer.preamble + str(image_id)

        image_birdseye_url = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + \
            commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(image_id) + '/' + \
            commandBirdsEye.postamble

        image_region_url = commandRegion.protocol.name + '://' + self.url_server + '/' + \
            commandRegion.application + '/' + commandRegion.preamble + '/' + str(image_id) + '/' + \
            commandRegion.postamble

        roi_list = list()
        datasets_list = list()
        projects_list = list()

        session = requests.Session()

        try:

            r = session.get(api_url)

        except Exception as e:

            print("Exception e : " + str(e))

            group_count = 0
            group_list = []

            data = {
                'server': self,
                'group': group,
                'projects': projects_list,
                'datasets': datasets_list,
                'image': image,
                'rois': roi_list
            }

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

        payload = {'limit': 300}
        rois_data = session.get(rois_url, params=payload).json()
        assert len(rois_data['data']) < 2000

        rmeta = rois_data['meta']
        roiCount = rmeta['totalCount']

        rdata = rois_data['data']

        for r in rdata:

            shapes = r['shapes']
            roi_id = r['@id']

            if roi_id == in_roi:

                for s in shapes:

                    shape_id = s['@id']

                    if shape_id == in_roi:

                        shape_type = s['@type']

                        types = shape_type.split('#')

                        type = types[1]

                        coordX = ''
                        coordY = ''
                        centreX = ''
                        centreY = ''
                        width = '0'
                        height = '0'

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
                            width = str(3192)
                            height = str(3192)

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

                shape = ({
                    'id': shape_id,
                    'type': type,
                    'shape_url': shape_url,
                    'viewer_url': viewer_url,
                    'x': coordX,
                    'y': coordY,
                    'centre_x': centreX,
                    'centre_y': centreY,
                    'width': width,
                    'height': height
                })

            roi = ({'id': roi_id, 'shape': shape})

        image_url = images_url + str(image_id)

        payload = {'limit': 300}
        image_data = session.get(image_url, params=payload).json()
        assert len(image_data['data']) < 2000

        data = image_data['data']
        name = data['Name']
        description = data.get('Description', '')
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

        dataset_url = datasets_url + str(image_id) + '/' + commandImageDatasets.postamble

        payload = {'limit': 300}
        dataset_data = session.get(dataset_url, params=payload).json()
        assert len(dataset_data['data']) < 2000

        ddata = dataset_data['data']

        datasets = list()
        projects = list()

        for p in ddata:

            dataset = ({
                'id': p['@id'],
                'name': p['Name']
            })

            projects_url = projects_url + str(p['@id']) + '/' + commandDatasetProjects.postamble

            payload = {'limit': 300}
            project_data = session.get(projects_url, params=payload).json()
            assert len(project_data['data']) < 2000

            pdata = project_data['data']

            for p in pdata:

                project = ({
                    'id': p['@id'],
                    'name': p['Name']
                })

                projects.append(project)

            datasets.append(dataset)

        data = {
            'server': self,
            'group': group,
            'projects': projects,
            'datasets': datasets,
            'image': image,
            'roi': roi
        }

        return data

    #
    #   Check the JSON Details for the Requested Image on Wordpress
    #
    def check_wordpress_image(self, user, image_id):

        Credential = apps.get_model('matrices', 'Credential')
        Command = apps.get_model('matrices', 'Command')

        credential = Credential.objects.get(username=user.username)
        commandWordpressImage = Command.objects.filter(type=self.type).get(name=CMD_API_WORDPRESS_IMAGE)

        image_url = commandWordpressImage.protocol.name + '://' + self.url_server + '/' + \
            commandWordpressImage.application + '/' + commandWordpressImage.preamble + '/' + str(image_id)

        token_str = credential.username + ':' + credential.apppwd
        encoded_token_str = token_str.encode('utf8')

        token = base64.standard_b64encode(encoded_token_str)
        headers = {'Authorization': 'Basic ' + token.decode('utf8')}

        data = {}

        try:

            response = requests.get(image_url, headers=headers, timeout=5)

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

            print("Exception e : " + str(e))

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

        data = {
            'image': image
        }

        return data

    #
    #   Check the JSON Details for the Requested Image
    #
    def check_imaging_server_image(self, image_id):

        Command = apps.get_model('matrices', 'Command')

        userid = self.uid

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        password = cipher.decrypt(self.pwd)

        commandAPI = Command.objects.filter(type=self.type).get(name=CMD_API_API)
        commandToken = Command.objects.filter(type=self.type).get(name=CMD_API_TOKEN)
        commandLogin = Command.objects.filter(type=self.type).get(name=CMD_API_LOGIN)

        commandImages = Command.objects.filter(type=self.type).get(name=CMD_API_IMAGES)
        commandImageROIs = Command.objects.filter(type=self.type).get(name=CMD_API_IMAGE_ROIS)

        commandViewer = ''

        if userid == "":

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_PUBLIC_VIEWER)

        else:

            commandViewer = Command.objects.filter(type=self.type).get(name=CMD_API_VIEWER)

        commandBirdsEye = Command.objects.filter(type=self.type).get(name=CMD_API_BIRDS_EYE)

        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'

        images_url = commandImages.protocol.name + '://' + self.url_server + '/' + commandImages.application + '/' + \
            commandImages.preamble + '/'
        imagerois_url = commandImageROIs.protocol.name + '://' + self.url_server + '/' + \
            commandImageROIs.application + '/' + commandImageROIs.preamble + '/'

        if userid == "":

            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                commandViewer.application + '/' + commandViewer.preamble + '/' + str(image_id)

        else:

            image_viewer_url = commandViewer.protocol.name + '://' + self.url_server + '/' + \
                commandViewer.application + '/' + commandViewer.preamble + str(image_id)

        image_birdseye_url = commandBirdsEye.protocol.name + '://' + self.url_server + '/' + \
            commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(image_id) + '/' +\
            commandBirdsEye.postamble

        session = requests.Session()

        try:

            r = session.get(api_url)

        except Exception as e:

            print("Exception e : " + str(e))

            data = {
                'image': image
            }

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

        payload = {'limit': 300}
        rois_data = session.get(rois_url, params=payload).json()
        assert len(rois_data['data']) < 2000

        rmeta = rois_data['meta']
        roiCount = rmeta['totalCount']

        image_url = images_url + str(image_id)

        try:

            payload = {'limit': 300}
            image_data = session.get(image_url, params=payload).json()
            assert len(image_data['data']) < 2000

        except Exception as e:

            print("Exception e : " + str(e))

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

            data = {
                'image': image
            }

            return data

        data = image_data['data']
        name = data['Name']
        description = data.get('Description', '')
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

        data = {
            'image': image
        }

        return data

    #
    #   Check the JSON Details for the Requested Image ROI
    #
    def check_imaging_server_image_roi(self, image_id, in_roi_id):

        Command = apps.get_model('matrices', 'Command')

        userid = self.uid

        cipher = AESCipher(config('CPW_CIPHER_STRING'))
        password = cipher.decrypt(self.pwd)

        commandAPI = Command.objects.filter(type=self.type).get(name=CMD_API_API)
        commandToken = Command.objects.filter(type=self.type).get(name=CMD_API_TOKEN)
        commandLogin = Command.objects.filter(type=self.type).get(name=CMD_API_LOGIN)

        commandImageROIs = Command.objects.filter(type=self.type).get(name=CMD_API_IMAGE_ROIS)

        api_url = commandAPI.protocol.name + '://' + self.url_server + '/' + commandAPI.application
        token_url = commandToken.protocol.name + '://' + self.url_server + '/' + commandToken.application + '/'
        login_url = commandLogin.protocol.name + '://' + self.url_server + '/' + commandLogin.application + '/'

        imagerois_url = commandImageROIs.protocol.name + '://' + self.url_server + '/' + \
            commandImageROIs.application + '/' + commandImageROIs.preamble + '/'

        session = requests.Session()

        roi = ({'id': ""})

        try:

            r = session.get(api_url)

        except Exception as e:

            print("Exception e : " + str(e))

            data = {
                'roi': roi
            }

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

        payload = {'limit': 300}
        rois_data = session.get(rois_url, params=payload).json()
        assert len(rois_data['data']) < 2000

        rmeta = rois_data['meta']
        roiCount = rmeta['totalCount']

        rdata = rois_data['data']

        for r in rdata:

            roi_id = r['@id']

            if in_roi_id == roi_id:

                roi = ({'id': roi_id})

        data = {
            'roi': roi
        }

        return data
