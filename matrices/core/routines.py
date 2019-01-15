# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os import urandom

from django.shortcuts import get_object_or_404

import json, urllib, requests, base64

from random import randint

from matrices.core.models import Matrix, Cell, Type, Protocol, Server, Command, Image
from matrices.core.models import Blog, Credential

from Crypto.Cipher import AES

from decouple import config

"""
	Encryption Methods
"""
def encrypt(plaintext):

	secret_key = config('ENCRYPT_KEY')

	cipher = AES.new(secret_key,AES.MODE_ECB) 

	encoded = base64.b64encode(cipher.encrypt(plaintext.rjust(32)))

	return encoded
		

def decrypt(ciphertext):

	secret_key = config('ENCRYPT_KEY')

	cipher = AES.new(secret_key,AES.MODE_ECB) 

	decoded = cipher.decrypt(base64.b64decode(ciphertext.strip())).strip()
	
	return decoded
	

"""
	Create a Blog Post
"""
def get_a_post_from_wordpress(user_name, post_id):

	credential = Credential.objects.get(username=user_name)

	blogGetPost = Blog.objects.get(name='PostAPost')

	get_post_url = blogGetPost.protocol.name + '://' + blogGetPost.url + '/' + blogGetPost.application + '/' + blogGetPost.preamble + '/' + post_id

	#print "get_post_url", get_post_url
	
	response = requests.get(get_post_url)

	data = response.json()

	#print 'Data', data

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
		'url': guid_rendered
		}

	return post


"""
	Create a Blog Post
"""
def get_a_post_comments_from_wordpress(user_name, post_id):

	blogGetPostComments = Blog.objects.get(name='GetPostComments')

	get_post_comments_url = blogGetPostComments.protocol.name + '://' + blogGetPostComments.url + '/' + blogGetPostComments.application + '/' + blogGetPostComments.preamble + post_id

	#print "get_post_comments_url", get_post_comments_url
	
	response = requests.get(get_post_comments_url)

	data = response.json()

	comment_list = list()

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
			'url': link
			}
		
		comment_list.append(comment)
	
	comment_list.reverse()
	
	return comment_list


"""
	Create a Blog Post
"""
def post_a_post_to_wordpress(user_name, title, content):

	credential = Credential.objects.get(username=user_name)

	blogPostAPost = Blog.objects.get(name='PostAPost')

	post_a_post_url = blogPostAPost.protocol.name + '://' + blogPostAPost.url + '/' + blogPostAPost.application + '/' + blogPostAPost.preamble

	#print "post_a_post_url", post_a_post_url
	
	token = base64.standard_b64encode(user_name + ':' + credential.apppwd)
	headers = {'Authorization': 'Basic ' + token}

	post = {'title': title,
		'content': content,
		'status': 'publish',
		'author': credential.wordpress,
		'format': 'standard'
		}

	response = requests.post(post_a_post_url, headers=headers, json=post)

	post_id = str(json.loads(response.content)['id'])

	return post_id


"""
	Create a Blog Post Comment
"""
def post_a_comment_to_wordpress(user_name, post_id, content):

	credential = Credential.objects.get(username=user_name)

	blogPostAComment = Blog.objects.get(name='PostAComment')

	post_a_comment_url = blogPostAComment.protocol.name + '://' + blogPostAComment.url + '/' + blogPostAComment.application + '/' + blogPostAComment.preamble
 
	#print "post_a_comment_url", post_a_comment_url
	
	token = base64.standard_b64encode(user_name + ':' + credential.apppwd)
	headers = {'Authorization': 'Basic ' + token}

	post = {
		'post': post_id,
		'content': content,
		'author': credential.wordpress,
		'format': 'standard'
		}

	response = requests.post(post_a_comment_url, headers=headers, json=post)

	return response


"""
	Delete a Blog Post
"""
def delete_a_post_from_wordpress(user_name, post_id):

	credential = Credential.objects.get(username=user_name)

	blogDeletePost = Blog.objects.get(name='DeletePost')

	delete_post_url = blogDeletePost.protocol.name + '://' + blogDeletePost.url + '/' + blogDeletePost.application + '/' + blogDeletePost.preamble + '/' + post_id

	#print "delete_post_url", delete_post_url
	
	token = base64.standard_b64encode(user_name + ':' + credential.apppwd)
	headers = {'Authorization': 'Basic ' + token}

	response = requests.delete(delete_post_url, headers=headers)

	return response


"""
	Get the JSON Details for the Requested Server
"""
def get_imaging_server_json(request, server_id):

	current_user = request.user

	server = get_object_or_404(Server, pk=server_id)
	
	commandAPI = Command.objects.filter(type=server.type).get(name='API')
	commandToken = Command.objects.filter(type=server.type).get(name='Token')
	commandLogin = Command.objects.filter(type=server.type).get(name='Login')
	commandProjects = Command.objects.filter(type=server.type).get(name='Projects')
	commandGroupProjects = Command.objects.filter(type=server.type).get(name='GroupProjects')
	commandGroupDatasets = Command.objects.filter(type=server.type).get(name='GroupDatasets')
	commandGroupImages = Command.objects.filter(type=server.type).get(name='GroupImages')
	commandDatasetImages = Command.objects.filter(type=server.type).get(name='DatasetImages')
	
	commandBirdsEye = Command.objects.filter(type=server.type).get(name='BirdsEye')

	api_url = commandAPI.protocol.name + '://' + server.url + '/' + commandAPI.application
	token_url = commandToken.protocol.name + '://' + server.url + '/' + commandToken.application + '/'
	login_url = commandLogin.protocol.name + '://' + server.url + '/' + commandLogin.application + '/'
	
	projects_url = commandProjects.protocol.name + '://' + server.url + '/' + commandProjects.application + '/' + commandProjects.preamble
	group_projects_url = commandGroupProjects.protocol.name + '://' + server.url + '/' + commandGroupProjects.application + '/' + commandGroupProjects.preamble
	datasets_url = commandGroupDatasets.protocol.name + '://' + server.url + '/' + commandGroupDatasets.application + '/' + commandGroupDatasets.preamble
	images_url = commandGroupImages.protocol.name + '://' + server.url + '/' + commandGroupImages.application + '/' + commandGroupImages.preamble
	dataset_images_url = commandDatasetImages.protocol.name + '://' + server.url + '/' + commandDatasetImages.application + '/' + commandDatasetImages.preamble
	
	#print "api_url", api_url
	#print "token_url", token_url
	#print "login_url", login_url
	
	session = requests.Session()
	session.timeout = 10
	
	try:
		r = session.get(api_url)

	except Exception as e:
		
		matrix_list = Matrix.objects.all
		image_list = Image.objects.filter(owner=current_user).filter(active=True)
		server_list = Server.objects.all

		group_count = 0
		group_list = []
	
		data = {'server': server, 'group_list': group_list, 'group_count': group_count, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }

		return data	

	token = session.get(token_url).json()['data']
	session.headers.update({'X-CSRFToken': token, 'Referer': login_url})
	
	userid = server.uid
	password = decrypt(server.pwd)

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
	
			matrix_list = Matrix.objects.all
			image_list = Image.objects.filter(owner=current_user).filter(active=True)
			server_list = Server.objects.all

			group_count = 0
			group_list = []
	
			data = {'server': server, 'group_list': group_list, 'group_count': group_count, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }

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

									randomImageBEURL = commandBirdsEye.protocol.name + '://' + server.url + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(randImageID) + '/' + commandBirdsEye.postamble

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

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	data = {'server': server, 'group_list': new_group_list, 'group_count': group_count, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }

	return data


"""
	Get the JSON Details for the Requested Group
"""
def get_imaging_server_group_json(request, server_id, group_id):

	server = get_object_or_404(Server, pk=server_id)
	
	current_user = request.user

	commandAPI = Command.objects.filter(type=server.type).get(name='API')
	commandToken = Command.objects.filter(type=server.type).get(name='Token')
	commandLogin = Command.objects.filter(type=server.type).get(name='Login')

	commandGroupProjects = Command.objects.filter(type=server.type).get(name='GroupProjects')
	commandProjects = Command.objects.filter(type=server.type).get(name='Projects')
	commandProjectsDatasets = Command.objects.filter(type=server.type).get(name='ProjectDatasets')
	
	commandDatasetImages = Command.objects.filter(type=server.type).get(name='DatasetImages')
	commandBirdsEye = Command.objects.filter(type=server.type).get(name='BirdsEye')
	
	api_url = commandAPI.protocol.name + '://' + server.url + '/' + commandAPI.application
	token_url = commandToken.protocol.name + '://' + server.url + '/' + commandToken.application + '/'
	login_url = commandLogin.protocol.name + '://' + server.url + '/' + commandLogin.application + '/'
	
	groups_url = commandGroupProjects.protocol.name + '://' + server.url + '/' + commandGroupProjects.application + '/' + commandGroupProjects.preamble
	projects_url = commandProjects.protocol.name + '://' + server.url + '/' + commandProjects.application + '/' + commandProjects.preamble + '/'
	datasets_url = commandProjectsDatasets.protocol.name + '://' + server.url + '/' + commandProjectsDatasets.application + '/' + commandProjectsDatasets.preamble + '/'
	
	images_url = commandDatasetImages.protocol.name + '://' + server.url + '/' + commandDatasetImages.application + '/' + commandDatasetImages.preamble + '/'

	#print "api_url", api_url
	#print "token_url", token_url
	#print "login_url", login_url
	
	session = requests.Session()

	try:
		r = session.get(api_url)

	except Exception as e:
		
		matrix_list = Matrix.objects.all
		image_list = Image.objects.filter(owner=current_user).filter(active=True)
		server_list = Server.objects.all

		group_count = 0
		group_list = []
	
		data = {'server': server, 'project_list': project_list, 'group': group, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }

		return data

	token = session.get(token_url).json()['data']
	session.headers.update({'X-CSRFToken': token, 'Referer': login_url})
	
	userid = server.uid
	password = decrypt(server.pwd)

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
	
			matrix_list = Matrix.objects.all
			image_list = Image.objects.filter(owner=current_user).filter(active=True)
			server_list = Server.objects.all

			groupCount = 0
			group_list = []
	
			data = {'server': server, 'project_list': project_list, 'group': group, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }

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
			assert len(project_data['data']) < 100
	
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
					
								randomImageBEURL = commandBirdsEye.protocol.name + '://' + server.url + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(randImageID) + '/' + commandBirdsEye.postamble
	
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
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	group = group_list[0]
	
	data = {'server': server, 'project_count': project_count, 'project_list': project_list, 'group': group, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list  }

	return data


"""
	Get the JSON Details for the Requested Project
"""
def get_imaging_server_project_json(request, server_id, project_id):
	
	server = get_object_or_404(Server, pk=server_id)
	
	current_user = request.user

	commandAPI = Command.objects.filter(type=server.type).get(name='API')
	commandToken = Command.objects.filter(type=server.type).get(name='Token')
	commandLogin = Command.objects.filter(type=server.type).get(name='Login')

	commandProjects = Command.objects.filter(type=server.type).get(name='Projects')
	commandProjectsDatasets = Command.objects.filter(type=server.type).get(name='ProjectDatasets')
	
	commandDatasetImages = Command.objects.filter(type=server.type).get(name='DatasetImages')
	commandBirdsEye = Command.objects.filter(type=server.type).get(name='BirdsEye')

	api_url = commandAPI.protocol.name + '://' + server.url + '/' + commandAPI.application
	token_url = commandToken.protocol.name + '://' + server.url + '/' + commandToken.application + '/'
	login_url = commandLogin.protocol.name + '://' + server.url + '/' + commandLogin.application + '/'
	
	projects_url = commandProjects.protocol.name + '://' + server.url + '/' + commandProjects.application + '/' + commandProjects.preamble + '/'
	datasets_url = commandProjectsDatasets.protocol.name + '://' + server.url + '/' + commandProjectsDatasets.application + '/' + commandProjectsDatasets.preamble + '/'
	
	images_url = commandDatasetImages.protocol.name + '://' + server.url + '/' + commandDatasetImages.application + '/' + commandDatasetImages.preamble + '/'

	#print "api_url", api_url
	#print "token_url", token_url
	#print "login_url", login_url
	
	session = requests.Session()

	try:
		r = session.get(api_url)

	except Exception as e:
	
		matrix_list = Matrix.objects.all
		image_list = Image.objects.filter(owner=current_user).filter(active=True)
		server_list = Server.objects.all

		group = ''
		project = ''
		dataset_list = []
	
		data = {'server': server, 'group': group, 'project': project, 'dataset_list': dataset_list, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list }
	
		return data

	token = session.get(token_url).json()['data']
	session.headers.update({'X-CSRFToken': token, 'Referer': login_url})
	
	userid = server.uid
	password = decrypt(server.pwd)

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
		assert len(image_data['data']) < 100
			
		for i in image_data['data']:
				
			if count == randImageIndex:
				randImageID = i['@id']
				randImageName = i['Name']
	
			count = count + 1
					
		randomImageBEURL = commandBirdsEye.protocol.name + '://' + server.url + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + str(randImageID) + '/' + commandBirdsEye.postamble

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

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	data = {'server': server, 'group': group, 'project': project, 'dataset_list': dataset_list, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list }
	
	return data


"""
	Get the JSON Details for the Requested Dataset
"""
def get_imaging_server_dataset_json(request, server_id, dataset_id):
	
	server = get_object_or_404(Server, pk=server_id)
	
	current_user = request.user

	userid = server.uid
	password = decrypt(server.pwd)

	if userid == "":
		commandViewer = Command.objects.filter(type=server.type).get(name='PublicViewer')
	else:
		commandViewer = Command.objects.filter(type=server.type).get(name='Viewer')

	commandAPI = Command.objects.filter(type=server.type).get(name='API')
	commandToken = Command.objects.filter(type=server.type).get(name='Token')
	commandLogin = Command.objects.filter(type=server.type).get(name='Login')

	commandDataset = Command.objects.filter(type=server.type).get(name='Dataset')
	commandDatasetProjects = Command.objects.filter(type=server.type).get(name='DatasetProjects')
	commandDatasetImages = Command.objects.filter(type=server.type).get(name='DatasetImages')

	commandThumbnail = Command.objects.filter(type=server.type).get(name='Thumbnail')
	commandBirdsEye = Command.objects.filter(type=server.type).get(name='BirdsEye')
	
	api_url = commandAPI.protocol.name + '://' + server.url + '/' + commandAPI.application
	token_url = commandToken.protocol.name + '://' + server.url + '/' + commandToken.application + '/'
	login_url = commandLogin.protocol.name + '://' + server.url + '/' + commandLogin.application + '/'
	
	datasets_url = commandDataset.protocol.name + '://' + server.url + '/' + commandDataset.application + '/' + commandDataset.preamble + '/'
	projects_url = commandDatasetProjects.protocol.name + '://' + server.url + '/' + commandDatasetProjects.application + '/' + commandDatasetProjects.preamble + '/'
	images_url = commandDatasetImages.protocol.name + '://' + server.url + '/' + commandDatasetImages.application + '/' + commandDatasetImages.preamble + '/'
	
	#print "api_url", api_url
	#print "token_url", token_url
	#print "login_url", login_url
	
	session = requests.Session()

	try:
		r = session.get(api_url)

	except Exception as e:
		
		matrix_list = Matrix.objects.all
		image_list = Image.objects.filter(owner=current_user).filter(active=True)
		server_list = Server.objects.all

		dataset = ''
		group = ''
		images_list = []
		project_list = []
	
		data = {'server': server, 'group': group, 'projects': project_list, 'images': images_list, 'dataset': dataset, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list }
	
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
	assert len(images_data['data']) < 100
	
	payload = {'limit': 100}
	dataset_data = session.get(dataset_url, params=payload).json()
	assert len(dataset_data['data']) < 100
	
	payload = {'limit': 100}
	projects_data = session.get(projects_url, params=payload).json()
	assert len(projects_data['data']) < 100
	
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
			image_viewer_url = commandViewer.protocol.name + '://' + server.url + '/' + commandViewer.application + '/' + commandViewer.preamble + '/' + image_id
		else:
			image_viewer_url = commandViewer.protocol.name + '://' + server.url + '/' + commandViewer.application + '/' + commandViewer.preamble + image_id

		image_birdseye_url = commandBirdsEye.protocol.name + '://' + server.url + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + image_id + '/' + commandBirdsEye.postamble
		image_thumbnail_url = commandThumbnail.protocol.name + '://' + server.url + '/' + commandThumbnail.application + '/' + commandThumbnail.preamble + '/' + image_id 

		image = ({
			'id': image_id, 
			'name': image_name,
			'viewer_url': image_viewer_url,
			'birdseye_url': image_birdseye_url,
			'thumbnail_url': image_thumbnail_url
			})
			
		images_list.append(image)
		
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	data = {'server': server, 'group': group, 'projects': project_list, 'images': images_list, 'dataset': dataset, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list }
	
	return data


"""
	Get the JSON Details for the Requested Image
"""
def get_imaging_server_image_json(request, server_id, image_id):
	
	current_user = request.user

	server = get_object_or_404(Server, pk=server_id)
	
	userid = server.uid
	password = decrypt(server.pwd)

	commandAPI = Command.objects.filter(type=server.type).get(name='API')
	commandToken = Command.objects.filter(type=server.type).get(name='Token')
	commandLogin = Command.objects.filter(type=server.type).get(name='Login')

	commandImages = Command.objects.filter(type=server.type).get(name='Images')
	commandImageDatasets = Command.objects.filter(type=server.type).get(name='ImageDatasets')
	commandImageROIs = Command.objects.filter(type=server.type).get(name='ImageROIs')

	commandDatasetProjects = Command.objects.filter(type=server.type).get(name='DatasetProjects')

	commandViewer = ''
	
	if userid == "":
		commandViewer = Command.objects.filter(type=server.type).get(name='PublicViewer')
	else:
		commandViewer = Command.objects.filter(type=server.type).get(name='Viewer')
	
	commandBirdsEye = Command.objects.filter(type=server.type).get(name='BirdsEye')
	commandRegion = Command.objects.filter(type=server.type).get(name='Region')

	api_url = commandAPI.protocol.name + '://' + server.url + '/' + commandAPI.application
	token_url = commandToken.protocol.name + '://' + server.url + '/' + commandToken.application + '/'
	login_url = commandLogin.protocol.name + '://' + server.url + '/' + commandLogin.application + '/'
	
	images_url = commandImages.protocol.name + '://' + server.url + '/' + commandImages.application + '/' + commandImages.preamble + '/'
	datasets_url = commandImageDatasets.protocol.name + '://' + server.url + '/' + commandImageDatasets.application + '/' + commandImageDatasets.preamble + '/'
	imagerois_url = commandImageROIs.protocol.name + '://' + server.url + '/' + commandImageROIs.application + '/' + commandImageROIs.preamble + '/'
	
	projects_url = commandDatasetProjects.protocol.name + '://' + server.url + '/' + commandDatasetProjects.application + '/' + commandDatasetProjects.preamble + '/'

	if userid == "":
		image_viewer_url = commandViewer.protocol.name + '://' + server.url + '/' + commandViewer.application + '/' + commandViewer.preamble + '/' + image_id
	else:
		image_viewer_url = commandViewer.protocol.name + '://' + server.url + '/' + commandViewer.application + '/' + commandViewer.preamble + image_id

	image_birdseye_url = commandBirdsEye.protocol.name + '://' + server.url + '/' + commandBirdsEye.application + '/' + commandBirdsEye.preamble + '/' + image_id + '/' + commandBirdsEye.postamble

	image_region_url = commandRegion.protocol.name + '://' + server.url + '/' + commandRegion.application + '/' + commandRegion.preamble + '/' + image_id + '/' + commandRegion.postamble
	
	#print "image_viewer_url", image_viewer_url
	#print "image_birdseye_url", image_birdseye_url
	
	#print "api_url", api_url
	#print "token_url", token_url
	#print "login_url", login_url
	
	session = requests.Session()

	try:
		r = session.get(api_url)

	except Exception as e:
		
		matrix_list = Matrix.objects.all
		image_list = Image.objects.filter(owner=current_user).filter(active=True)
		server_list = Server.objects.all

		group_count = 0
		group_list = []
	
		data = {'server': server, 'group': group, 'projects': projects, 'datasets': datasets, 'image': image, 'rois': roi_list, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list }
	
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
	assert len(rois_data['data']) < 100
	
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
			width = '0'
			height = '0'
			
			#print 'type', type
			
			if type == 'Point':
	
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
	
				intCoordX = int(s['X'])
				intCoordY = int(s['Y'])
				intWidth = int(s['Width'])
				intHeight = int(s['Height'])
		
				coordX = str(intCoordX)
				coordY = str(intCoordY)
				width = str(intWidth)
				height = str(intHeight)
		
			if type == 'Ellipse':
	
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
				
				intWidth = maxX - minX
				intHeight = maxY - minY
				
				width = str(intWidth)
				height = str(intHeight)
			
			if int(width) > 3192 or int(height) > 3192:
			
				middleX = int(coordX) + ( int(width) / 2 )
				middleY = int(coordY) + ( int(height) / 2 )
			
				intX = middleX - ( 3192 / 2 )
				intY = middleY - ( 3192 / 2 )
			
				coordX = str(intX)
				coordY = str(intY)
				
				width = "3192"
				height = "3192"

			shape_url = image_region_url + coordX + ',' + coordY + ',' + width + ',' + height
			#print shape_url
			
			shape = ({'id': shape_id, 'type': type, 'shape_url': shape_url, 'x': coordX, 'y': coordY, 'width': width, 'height': height })
			
			shape_list.append(shape)
		
		roi = ({'id': roi_id, 'shapes': shape_list})
	
		roi_list.append(roi)


	image_url = images_url + image_id
	#print image_url

	payload = {'limit': 100}
	image_data = session.get(image_url, params=payload).json()
	assert len(image_data['data']) < 100
	
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
	assert len(dataset_data['data']) < 100
	
	ddata = dataset_data['data']
	
	datasets = list()
	projects = list()
	
	for p in ddata:
		dataset = ({'id': p['@id'], 'name': p['Name']})
		
		projects_url = projects_url + str(p['@id']) + '/' + commandDatasetProjects.postamble
		
		#print 'projects_url', projects_url

		payload = {'limit': 100}
		project_data = session.get(projects_url, params=payload).json()
		assert len(project_data['data']) < 100

		pdata = project_data['data']

		for p in pdata:
			project = ({'id': p['@id'], 'name': p['Name']})
			projects.append(project)

		datasets.append(dataset)
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	data = {'server': server, 'group': group, 'projects': projects, 'datasets': datasets, 'image': image, 'rois': roi_list, 'matrix_list': matrix_list, 'server_list': server_list, 'image_list': image_list }

	return data


"""
	Generate the Matrix
"""
def generateMatrix(matrix_id):

	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)
	
	columnCount = countColumns(matrix_id)
	rowCount = countRows(matrix_id)
	
	cells = generateCells(matrix_id)

	matrix_cells=[[0 for cc in range(columnCount)] for rc in range(rowCount)]

	for i, row in enumerate(rows):
	
		row_cells=cells.filter(ycoordinate=i)
		
		for j, column in enumerate(columns):
			
			matrix_cell = row_cells.filter(xcoordinate=j)[0]
			matrix_cells[i][j] = matrix_cell

	return matrix_cells


"""
	Get the Rows in Matrix
"""
def generateRows(matrix_id):

	rows = Cell.objects.filter(matrix=matrix_id).values('ycoordinate').distinct()

	return rows


"""
	Get the Columns in Matrix
"""
def generateColumns(matrix_id):

	columns = Cell.objects.filter(matrix=matrix_id).values('xcoordinate').distinct()

	return columns


"""
	Count Rows in Matrix
"""
def countRows(matrix_id):

	rowCount = Cell.objects.filter(matrix=matrix_id).values('ycoordinate').distinct().count()

	return rowCount


"""
	Count Columns in Matrix
"""
def countColumns(matrix_id):

	columnCount = Cell.objects.filter(matrix=matrix_id).values('xcoordinate').distinct().count()

	return columnCount


"""
	Get Cells in Matrix
"""
def generateCells(matrix_id):

	cells = Cell.objects.filter(matrix=matrix_id)

	return cells
