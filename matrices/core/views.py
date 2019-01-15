# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse

from django.template import loader

from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render, redirect

from django.core.urlresolvers import reverse

from django.views import generic

from django.forms.models import inlineformset_factory

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages 

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template.loader import render_to_string

from django.contrib.auth.hashers import make_password, check_password

from matrices.core.forms import SignUpForm
from matrices.core.tokens import account_activation_token

from matrices.core.forms import MatrixForm, CellForm, HeaderForm, CommandForm, ServerForm, CommentForm
from matrices.core.forms import BlogForm, CredentialForm
from matrices.core.forms import ProtocolForm, TypeForm, EditUserForm

from matrices.core.models import Matrix, Cell, Type, Protocol, Server, Command, Image
from matrices.core.models import Blog, Credential

from .routines import generateMatrix, generateRows, generateColumns, countRows
from .routines import countColumns, generateCells, get_imaging_server_json

from .routines import get_imaging_server_group_json
from .routines import get_imaging_server_project_json
from .routines import get_imaging_server_dataset_json
from .routines import get_imaging_server_image_json

from .routines import encrypt, decrypt

from .routines import get_a_post_from_wordpress
from .routines import get_a_post_comments_from_wordpress
from .routines import post_a_post_to_wordpress
from .routines import post_a_comment_to_wordpress
from .routines import delete_a_post_from_wordpress

import requests

#
# HOME VIEW
#
def home(request):

	if request.user.is_anonymous():

		matrix_list = []
		image_list = []
		server_list = []
	
	else:
	
		current_user = request.user
	
		matrix_list = Matrix.objects.all
		image_list = Image.objects.filter(owner=current_user).filter(active=True)
		server_list = Server.objects.all

	data = { 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'home.html', data)


#
# VIEWS FOR AUTHORIZATION
#
def signup(request):

	if request.method == 'POST':

		form = SignUpForm(request.POST)

		if form.is_valid():

			user = form.save(commit=False)
			#user.is_active = True
			user.is_active = False
			user.save()

			current_site = get_current_site(request)

			subject = 'Activate Your Comparative Pathology Workbench Account'

			message = render_to_string('user/account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})

			user.email_user(subject, message)

			#return HttpResponseRedirect(reverse('matrices:home', args=()))						
			#return redirect('matrices:home')
			return redirect('account_activation_sent')

	else:

		form = SignUpForm()

	return render(request, 'user/signup.html', {'form': form})


def account_activation_sent(request):

	return render(request, 'user/account_activation_sent.html')


def activate(request, uidb64, token):

	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):

		user.is_active = True
		user.profile.email_confirmed = True
		user.save()
		login(request, user)

		return HttpResponseRedirect(reverse('matrices:home', args=()))						
		#return redirect('matrices:home')

	else:

		return render(request, 'user/account_activation_invalid.html')


#
# VIEWS FOR HOSTS
#
@login_required
def list_image_cart(request):

	current_user = request.user
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	data = { 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/list_image_cart.html', data)
	

@login_required
def list_imaging_hosts(request):

	current_user = request.user
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	data = { 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/list_imaging_hosts.html', data)
	

@login_required
def maintenance(request):

	current_user = request.user
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	type_list = Type.objects.all
	protocol_list = Protocol.objects.all
	command_list = Command.objects.all
	user_list = User.objects.all
	blog_list = Blog.objects.all
	credential_list = Credential.objects.all

	data = { 'user_list': user_list, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list, 'type_list': type_list, 'protocol_list': protocol_list, 'command_list': command_list, 'blog_list': blog_list, 'credential_list': credential_list }

	return render(request, 'host/maintenance.html', data)
	

@login_required
def authorisation(request):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	user_list = User.objects.all

	data = { 'user_list': user_list, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/authorisation.html', data)
	

@login_required
def view_user(request, user_id):

	current_user = request.user

	user = get_object_or_404(User, pk=user_id)

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	data = { 'user_id': user_id, 'user': user, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/detail_user.html', data)


@login_required
def edit_user(request, user_id):

	current_user = request.user

	user = get_object_or_404(User, pk=user_id)
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True:

		if request.method == "POST":
	
			form = EditUserForm(request.POST, instance=user)
			
			if form.is_valid():
			
				user = form.save(commit=False)

				user.save()
						
				return HttpResponseRedirect(reverse('matrices:authorisation', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = EditUserForm(instance=user)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/edit_user.html', data)
	
	
@login_required
def delete_user(request, user_id):

	current_user = request.user

	user = get_object_or_404(User, pk=user_id)
	
	if current_user.is_superuser == True:

		user.delete()
	
	return HttpResponseRedirect(reverse('matrices:authorisation', args=()))						


@login_required
def new_blog_command(request):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True:
	
		if request.method == "POST":
	
			form = BlogForm(request.POST)
		
			if form.is_valid():
		
				blog = form.save(commit=False)

				blog.owner_id = current_user.id

				blog.save()

				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))
		
			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = BlogForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/new_blog_command.html', data)

	
@login_required
def view_blog_command(request, blog_id):

	current_user = request.user

	blog = get_object_or_404(Blog, pk=blog_id)

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	owner = get_object_or_404(User, pk=blog.owner_id)

	data = { 'owner': owner, 'blog_id': blog_id, 'blog': blog, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/detail_blog_command.html', data)
	

@login_required
def edit_blog_command(request, blog_id):

	current_user = request.user

	blog = get_object_or_404(Blog, pk=blog_id)
	
	owner = get_object_or_404(User, pk=blog.owner_id)
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True or blog.owner_id == current_user.id:

		if request.method == "POST":
	
			form = BlogForm(request.POST, instance=blog)
			
			if form.is_valid():
			
				blog = form.save(commit=False)

				blog.owner_id = current_user.id

				blog.save()
						
				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = BlogForm(instance=blog)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/edit_blog_command.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						


@login_required
def delete_blog_command(request, blog_id):

	current_user = request.user

	blog = get_object_or_404(Blog, pk=blog_id)
	
	owner = get_object_or_404(User, pk=blog.owner_id)
	
	if current_user.is_superuser == True or blog.owner_id == current_user.id:

		blog.delete()
	
	return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						


@login_required
def new_blog_credential(request):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True:
	
		if request.method == "POST":
	
			form = CredentialForm(request.POST)
		
			if form.is_valid():
		
				credential = form.save(commit=False)

				credential.owner_id = current_user.id

				credential.save()

				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))
		
			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = CredentialForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/new_blog_credential.html', data)

	
@login_required
def view_blog_credential(request, credential_id):

	current_user = request.user

	credential = get_object_or_404(Credential, pk=credential_id)

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	owner = get_object_or_404(User, pk=credential.owner_id)

	data = { 'owner': owner, 'credential_id': credential_id, 'credential': credential, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/detail_blog_credential.html', data)
	

@login_required
def edit_blog_credential(request, credential_id):

	current_user = request.user

	credential = get_object_or_404(Credential, pk=credential_id)
	
	owner = get_object_or_404(User, pk=credential.owner_id)
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True or credential.owner_id == current_user.id:

		if request.method == "POST":
	
			form = CredentialForm(request.POST, instance=credential)
			
			if form.is_valid():
			
				credential = form.save(commit=False)

				credential.owner_id = current_user.id

				credential.save()
						
				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = CredentialForm(instance=credential)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/edit_blog_credential.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						


@login_required
def delete_blog_credential(request, credential_id):

	current_user = request.user

	credential = get_object_or_404(Credential, pk=credential_id)
	
	owner = get_object_or_404(User, pk=credential.owner_id)
	
	if current_user.is_superuser == True or credential.owner_id == current_user.id:

		credential.delete()
	
	return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						


@login_required
def new_type(request):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True:
	
		if request.method == "POST":
		
			form = TypeForm(request.POST)
		
			if form.is_valid():
		
				type = form.save(commit=False)

				type.owner_id = current_user.id

				type.save()

				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						
		
			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = TypeForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/new_type.html', data)

	
@login_required
def view_type(request, type_id):

	current_user = request.user

	type = get_object_or_404(Type, pk=type_id)

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	owner = get_object_or_404(User, pk=type.owner_id)

	data = { 'owner': owner, 'type_id': type_id, 'type': type, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/detail_type.html', data)
	

@login_required
def edit_type(request, type_id):

	current_user = request.user

	type = get_object_or_404(Type, pk=type_id)
	
	owner = get_object_or_404(User, pk=type.owner_id)
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True or type.owner_id == current_user.id:

		if request.method == "POST":
	
			form = TypeForm(request.POST, instance=type)
			
			if form.is_valid():
			
				type = form.save(commit=False)

				type.owner_id = current_user.id

				type.save()
						
				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = TypeForm(instance=type)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/edit_type.html', data)
	


@login_required
def delete_type(request, type_id):

	current_user = request.user

	type = get_object_or_404(Type, pk=type_id)
	
	owner = get_object_or_404(User, pk=type.owner_id)
	
	if current_user.is_superuser == True or type.owner_id == current_user.id:

		type.delete()
	
	return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						



@login_required
def new_command(request):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True:
	
		if request.method == "POST":
	
			form = CommandForm(request.POST)
		
			if form.is_valid():
		
				command = form.save(commit=False)

				command.owner_id = current_user.id

				command.save()

				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))
		
			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = CommandForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/new_command.html', data)

	
@login_required
def view_command(request, command_id):

	current_user = request.user

	command = get_object_or_404(Command, pk=command_id)

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	owner = get_object_or_404(User, pk=command.owner_id)

	data = { 'owner': owner, 'command_id': command_id, 'command': command, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/detail_command.html', data)
	

@login_required
def edit_command(request, command_id):

	current_user = request.user

	command = get_object_or_404(Command, pk=command_id)
	
	owner = get_object_or_404(User, pk=command.owner_id)
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True or command.owner_id == current_user.id:

		if request.method == "POST":
	
			form = CommandForm(request.POST, instance=command)
			
			if form.is_valid():
			
				command = form.save(commit=False)

				command.owner_id = current_user.id

				command.save()
						
				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = CommandForm(instance=command)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/edit_command.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						


@login_required
def delete_command(request, command_id):

	current_user = request.user

	command = get_object_or_404(Command, pk=command_id)
	
	owner = get_object_or_404(User, pk=command.owner_id)
	
	if current_user.is_superuser == True or command.owner_id == current_user.id:

		command.delete()
	
	return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						



@login_required
def new_protocol(request):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True:
	
		if request.method == "POST":
	
			form = ProtocolForm(request.POST)
		
			if form.is_valid():
		
				protocol = form.save(commit=False)

				protocol.owner_id = current_user.id

				protocol.save()

				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						
		
			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = ProtocolForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/new_protocol.html', data)

	
@login_required
def view_protocol(request, protocol_id):

	current_user = request.user

	protocol = get_object_or_404(Protocol, pk=protocol_id)

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	owner = get_object_or_404(User, pk=protocol.owner_id)

	data = { 'owner': owner, 'protocol_id': protocol_id, 'protocol': protocol, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/detail_protocol.html', data)
	

@login_required
def edit_protocol(request, protocol_id):

	current_user = request.user

	protocol = get_object_or_404(Protocol, pk=protocol_id)
	
	owner = get_object_or_404(User, pk=protocol.owner_id)
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True or protocol.owner_id == current_user.id:

		if request.method == "POST":
	
			form = ProtocolForm(request.POST, instance=protocol)
			
			if form.is_valid():
			
				protocol = form.save(commit=False)

				protocol.owner_id = current_user.id

				protocol.save()
				
				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = ProtocolForm(instance=protocol)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/edit_protocol.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						



@login_required
def delete_protocol(request, protocol_id):

	current_user = request.user

	protocol = get_object_or_404(Protocol, pk=protocol_id)
	
	owner = get_object_or_404(User, pk=protocol.owner_id)
	
	if current_user.is_superuser == True or protocol.owner_id == current_user.id:

		protocol.delete()
	
	return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						



@login_required
def new_server(request):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	if request.method == "POST":
	
		form = ServerForm(request.POST)
		
		if form.is_valid():
		
			server = form.save(commit=False)

			server.owner_id = current_user.id

			encryptedPwd = encrypt(server.pwd)
					
			server.pwd = encryptedPwd

			server.save()

			return HttpResponseRedirect(reverse('matrices:list_imaging_hosts', args=()))						

		else:

			messages.error(request, "Error")

			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	else:

		form = ServerForm()

		data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/new_server.html', data)

	
@login_required
def view_server(request, server_id):

	current_user = request.user

	server = get_object_or_404(Server, pk=server_id)

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	owner = get_object_or_404(User, pk=server.owner_id)

	data = { 'owner': owner, 'server_id': server_id, 'server': server, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/detail_server.html', data)
	

@login_required
def edit_server(request, server_id):

	current_user = request.user

	server = get_object_or_404(Server, pk=server_id)
	
	owner = get_object_or_404(User, pk=server.owner_id)
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if current_user.is_superuser == True or server.owner_id == current_user.id:

		if request.method == "POST":
	
			form = ServerForm(request.POST, instance=server)
			
			if form.is_valid():
			
				server = form.save(commit=False)

				encryptedPwd = encrypt(server.pwd)
				
				server.pwd = encryptedPwd
				
				server.owner_id = current_user.id

				server.save()
				
				return HttpResponseRedirect(reverse('matrices:list_imaging_hosts', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = ServerForm(instance=server)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/edit_server.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:list_imaging_hosts', args=()))						



@login_required
def delete_server(request, server_id):

	current_user = request.user

	server = get_object_or_404(Server, pk=server_id)
	
	owner = get_object_or_404(User, pk=server.owner_id)
	
	if current_user.is_superuser == True or server.owner_id == current_user.id:

		server.delete()
	
	return HttpResponseRedirect(reverse('matrices:list_imaging_hosts', args=()))						


#
# VIEWS FOR GALLERY
#
@login_required
def add_image(request, server_id, image_id, roi_id):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	server = get_object_or_404(Server, pk=server_id)
	
	image_count = Image.objects.filter(identifier=image_id).filter(active=True).count()

	data = get_imaging_server_image_json(request, server_id, image_id)
	
	json_image = data['image']
	name = json_image['name']
	viewer_url = json_image['viewer_url']
	birdseye_url = json_image['birdseye_url']

	if roi_id == '0':
		
		image = Image(identifier=image_id, name=name, server=server, viewer_url=viewer_url, birdseye_url=birdseye_url, owner=current_user, active=True, roi=0)
		image.save()

	else:
	
		json_rois = data['rois']
		
		for rois in json_rois:
		
			for shape in rois['shapes']:
			
				if shape['id'] == int(roi_id):
			
					viewer_url = shape['shape_url']
					birdseye_url = shape['shape_url']
				
					print 'shape_url', shape['shape_url']
					
					image = Image(identifier=image_id, name=name, server=server, viewer_url=viewer_url, birdseye_url=birdseye_url, owner=current_user, active=True, roi=roi_id)
					image.save()
					
	return HttpResponseRedirect(reverse('matrices:webgallery_show_image', args=(server_id, image_id)))				
	

@login_required
def delete_image(request, image_id):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	image = get_object_or_404(Image, pk=image_id)
	
	image.delete()
					
	return HttpResponseRedirect(reverse('matrices:list_image_cart', args=()))				
	

@login_required()
def show_imaging_server(request, server_id):
	"""
	Show the Imaging Server
	"""

	data = get_imaging_server_json(request, server_id)

	return render(request, 'gallery/show_server.html', data)


@login_required()
def show_group(request, server_id, group_id):
	"""
	Show a group
	"""

	data = get_imaging_server_group_json(request, server_id, group_id)
	
	return render(request, 'gallery/show_group.html', data)


@login_required()
def show_project(request, server_id, project_id):
	"""
	Show a project
	"""
	
	data = get_imaging_server_project_json(request, server_id, project_id)

	return render(request, 'gallery/show_project.html', data)


@login_required()
def show_dataset(request, server_id, dataset_id):
	"""
	Show a dataset
	"""
	
	data = get_imaging_server_dataset_json(request, server_id, dataset_id)
	
	return render(request, 'gallery/show_dataset.html', data)

	
@login_required()
def show_image(request, server_id, image_id):
	"""
	Show an image
	"""
	
	data = get_imaging_server_image_json(request, server_id, image_id)

	#print 'data', data

	return render(request, 'gallery/show_image.html', data)


#
# VIEWS FOR MATRICES
#
@login_required
def index_matrix(request):

	current_user = request.user

	matrix_list = Matrix.objects.all().select_related('owner')
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	data = { 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'matrices/index.html', data)
	

@login_required
def matrix(request, matrix_id):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)

	credential = Credential.objects.get(username=request.user.username)
	
	matrix_link = 'matrix_link'	
	
	if credential != []:

		if credential.apppwd == '':

			matrix_link = ''	

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	data = { 'matrix_link': matrix_link, 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'matrices/matrix.html', data)
	

@login_required
def list_matrix(request):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	data = { 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'matrices/index.html', data)
	

@login_required
def new_matrix(request):

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if request.method == "POST":
	
		form = MatrixForm(request.POST)
		
		if form.is_valid():
		
			matrix = form.save(commit=False)

			credential = Credential.objects.get(username=request.user.username)
	
			post_id = ''
			
			if credential != []:

				if credential.apppwd != '':

					post_id = post_a_post_to_wordpress(request.user.username, matrix.title, matrix.description)

			matrix.blogpost = post_id

			matrix.owner_id = current_user.id

			matrix.save()

			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix.id,)))				

		else:
		
			messages.error(request, "Error")

			data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
	else:
	
		form = MatrixForm()

		data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'matrices/new_matrix.html', data)

	
@login_required
def view_matrix_blog(request, matrix_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)

	current_user = request.user

	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	owner = get_object_or_404(User, pk=matrix.owner_id)

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	blogpost = get_a_post_from_wordpress(request.user.username, matrix.blogpost)

	comment_list = list()
	
	comment_list = get_a_post_comments_from_wordpress(request.user.username, matrix.blogpost)

	
	if request.method == "POST":
	
		form = CommentForm(request.POST)
			
		if form.is_valid():

			cd = form.cleaned_data
				
			comment = cd.get('comment')
				
			if comment != '':
				
				response = post_a_comment_to_wordpress(request.user.username, matrix.blogpost, comment)
				
			return HttpResponseRedirect(reverse('matrices:detail_matrix_blog', args=(matrix_id,)))						

		else:
			
			messages.error(request, "Error")
	
	else:
	
		form = CommentForm()
			
	
	data = { 'form': form, 'owner': owner, 'matrix_id': matrix_id, 'matrix': matrix, 'blogpost': blogpost, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list, 'comment_list': comment_list }

	return render(request, 'matrices/detail_matrix_blog.html', data)


@login_required
def view_matrix(request, matrix_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)

	#print 'Matrix', matrix
	
	blogLinkPost = Blog.objects.get(name='LinkPost')

	link_post_url = blogLinkPost.protocol.name + '://' + blogLinkPost.url + '/' + blogLinkPost.application + '/' + matrix.blogpost

	matrix_link = link_post_url
	
	current_user = request.user
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	owner = get_object_or_404(User, pk=matrix.owner_id)

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	data = { 'owner': owner, 'matrix_id': matrix_id, 'matrix': matrix, 'matrix_link': matrix_link, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'matrices/detail_matrix.html', data)
	

@login_required
def edit_matrix(request, matrix_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	if matrix.owner_id == current_user.id:

		if request.method == "POST":
	
			form = MatrixForm(request.POST, instance=matrix)
			
			if form.is_valid():
			
				matrix = form.save(commit=False)

				matrix.owner_id = current_user.id

				post_id = ''
				
				if matrix.blogpost == '':
				
					credential = Credential.objects.get(username=request.user.username)
	
					if credential != []:

						if credential.apppwd != '':

							post_id = post_a_post_to_wordpress(request.user.username, matrix.title, matrix.description)

				matrix.blogpost = post_id

				matrix.save()
				
				matrix_list = Matrix.objects.all

				matrix_cells = generateMatrix(matrix_id)
				columns = generateColumns(matrix_id)
				rows = generateRows(matrix_id)
							
				data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
				
				return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

		else:
	
			form = MatrixForm(instance=matrix)
			
		return render(request, 'matrices/edit_matrix.html', {'owner': owner, 'form': form, 'matrix': matrix, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list, })
	
	else:

		matrix_list = Matrix.objects.all
	
		matrix_cells = generateMatrix(matrix_id)
		columns = generateColumns(matrix_id)
		rows = generateRows(matrix_id)
					
		data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))				



@login_required
def delete_matrix(request, matrix_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	if matrix.owner_id == current_user.id:

		oldCells = Cell.objects.filter(matrix=matrix_id)

		for oldCell in oldCells:
		
			if oldCell.image is not None:
				
				image = Image.objects.get(id=oldCell.image.id)
				
				image.active = True
				
				image.save()

			if oldCell.blogpost != '':
			
				credential = Credential.objects.get(username=request.user.username)
	
				if credential != []:

					if credential.apppwd != '':

						response = delete_a_post_from_wordpress(request.user.username, oldCell.blogpost)

		if matrix.blogpost != '':

			credential = Credential.objects.get(username=request.user.username)
	
			if credential != []:

				if credential.apppwd != '':

					response = delete_a_post_from_wordpress(request.user.username, matrix.blogpost)

		matrix.delete()
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	data = { 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
	return HttpResponseRedirect(reverse('matrices:index', args=()))


@login_required
def edit_cell(request, matrix_id, cell_id):

	cell = get_object_or_404(Cell, pk=cell_id)
				
	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	if matrix.owner_id == current_user.id:

		if request.method == "POST":
	
			if cell.xcoordinate == 0 or cell.ycoordinate == 0:

				form = HeaderForm(request.POST, instance=cell)

				if form.is_valid():
						
					cell = form.save(commit=False)
				
					cell.matrix_id = matrix_id
			
					cell.save()

				else:
			
					messages.error(request, "Error")
	
					data = { 'form': form, 'matrix': matrix, 'cell': cell, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
				
					return render(request, 'matrices/edit_cell.html', data)

			else:
			
				imageOld = Image.objects.none
				imageNew = Image.objects.none
				
				if cell.image is None:
			
					form = CellForm(request.user.id, None, request.POST, instance=cell)
					
				else:

					form = CellForm(request.user.id, cell.image.id, request.POST, instance=cell)
						
					imageOld = Image.objects.get(pk=cell.image.id)
	
					imageOld.active = True
				
					imageOld.save()

				if form.is_valid():
						
					imageNew = get_object_or_404(Image, pk=cell.image.id)
				
					imageNew.active = False
				
					imageNew.save()
						
					cell = form.save(commit=False)
				
					cell.matrix_id = matrix_id
					
					post_id = ''
				
					if cell.blogpost == '':
				
						credential = Credential.objects.get(username=request.user.username)
	
						if credential != []:

							if credential.apppwd != '':

								post_id = post_a_post_to_wordpress(request.user.username, cell.title, cell.description)

					cell.blogpost = post_id

					cell.save()

				else:
			
					messages.error(request, "Error")
	
					data = { 'form': form, 'matrix': matrix, 'cell': cell, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
				
					return render(request, 'matrices/edit_cell.html', data)
				
			matrix_cells = generateMatrix(matrix_id)
			columns = generateColumns(matrix_id)
			rows = generateRows(matrix_id)
			
			data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
			#return render(request, 'matrices/matrix.html', data)
			
			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))				

		else:
	
			if cell.xcoordinate == 0 or cell.ycoordinate == 0:

				form = HeaderForm(instance=cell)

			else:

				if cell.image is None:
			
					form = CellForm(request.user.id, None, instance=cell)
					
				else:

					form = CellForm(request.user.id, cell.image.id, instance=cell)

		return render(request, 'matrices/edit_cell.html', {'form': form, 'matrix': matrix, 'cell': cell, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list })

	else:

		matrix_list = Matrix.objects.all
		image_list = Image.objects.filter(owner=current_user).filter(active=True)
		server_list = Server.objects.all
			
		matrix_cells = generateMatrix(matrix_id)
		columns = generateColumns(matrix_id)
		rows = generateRows(matrix_id)
					
		data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))		


@login_required
def view_cell(request, matrix_id, cell_id):
	
	current_user = request.user

	cell = get_object_or_404(Cell, pk=cell_id)
	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	blogLinkPost = Blog.objects.get(name='LinkPost')

	link_post_url = blogLinkPost.protocol.name + '://' + blogLinkPost.url + '/' + blogLinkPost.application + '/' + cell.blogpost

	cell_link = link_post_url
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
	
	return render(request, 'matrices/detail_cell.html', {'cell': cell, 'cell_link': cell_link, 'matrix': matrix, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list })


@login_required
def view_cell_blog(request, matrix_id, cell_id):
	
	current_user = request.user

	cell = get_object_or_404(Cell, pk=cell_id)
	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	blogpost = get_a_post_from_wordpress(request.user.username, cell.blogpost)

	comment_list = list()
	
	comment_list = get_a_post_comments_from_wordpress(request.user.username, cell.blogpost)
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all
		
	if request.method == "POST":
	
		form = CommentForm(request.POST)
			
		if form.is_valid():

			cd = form.cleaned_data
				
			comment = cd.get('comment')
				
			if comment != '':
				
				response = post_a_comment_to_wordpress(request.user.username, cell.blogpost, comment)
				
			return HttpResponseRedirect(reverse('matrices:view_cell_blog', args=(matrix_id, cell_id)))						

		else:
			
			messages.error(request, "Error")
	
	else:
	
		form = CommentForm()

	data = { 'form': form, 'matrix_id': matrix_id, 'cell': cell, 'matrix': matrix, 'blogpost': blogpost, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list, 'comment_list': comment_list }

	return render(request, 'matrices/detail_cell_blog.html', data)


@login_required
def add_cell(request, matrix_id):

	current_user = request.user

	matrix = Matrix.objects.get(id=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)

	cell1 = Cell(matrix=matrix, title="", description="", xcoordinate=0, ycoordinate=0)
	cell1.save()
	cell2 = Cell(matrix=matrix, title="", description="", xcoordinate=0, ycoordinate=1)
	cell2.save()
	cell3 = Cell(matrix=matrix, title="", description="", xcoordinate=1, ycoordinate=0)
	cell3.save()
	cell4 = Cell(matrix=matrix, title="", description="", xcoordinate=1, ycoordinate=1)
	cell4.save()


	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))
	

@login_required
def add_column(request, matrix_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	if matrix.owner_id == current_user.id:

		matrix = Matrix.objects.get(id=matrix_id)
	
		nextColumn = Cell.objects.filter(matrix=matrix_id).values('xcoordinate').distinct().count()
		rows = Cell.objects.filter(matrix=matrix_id).values('ycoordinate').distinct()
	
		for i, row in enumerate(rows):

			cell = Cell(matrix=matrix, title="", description="", xcoordinate=nextColumn, ycoordinate=i)
			cell.save()


	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)
					
	data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }
			
	return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))				
	

@login_required
def add_column_left(request, matrix_id, column_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	if matrix.owner_id == current_user.id:

		matrix = Matrix.objects.get(id=matrix_id)
	
		oldCells = Cell.objects.filter(matrix=matrix_id).filter(xcoordinate__gte=column_id)
		rows = Cell.objects.filter(matrix=matrix_id).values('ycoordinate').distinct()
	
		for oldcell in oldCells:
		
			oldcell.xcoordinate += 1
			oldcell.save()

		for i, row in enumerate(rows):

			cell = Cell(matrix=matrix, title="", description="", xcoordinate=column_id, ycoordinate=i)
			cell.save()


	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))
	

@login_required
def add_column_right(request, matrix_id, column_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	if matrix.owner_id == current_user.id:

		matrix = Matrix.objects.get(id=matrix_id)
	
		oldCells = Cell.objects.filter(matrix=matrix_id).filter(xcoordinate__gt=column_id)
		rows = Cell.objects.filter(matrix=matrix_id).values('ycoordinate').distinct()
	
		for oldcell in oldCells:
		
			oldcell.xcoordinate += 1
			oldcell.save()

		new_column_id = int(column_id) + 1
	
		for i, row in enumerate(rows):

			cell = Cell(matrix=matrix, title="", description="", xcoordinate=new_column_id, ycoordinate=i)
			cell.save()


	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))
	

@login_required
def add_row(request, matrix_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	if matrix.owner_id == current_user.id:

		matrix = Matrix.objects.get(id=matrix_id)
	
		nextRow = Cell.objects.filter(matrix=matrix_id).values('ycoordinate').distinct().count()
		columns = Cell.objects.filter(matrix=matrix_id).values('xcoordinate').distinct()
	
		for i, column in enumerate(columns):

			cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=nextRow)
			cell.save()


	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))
	

@login_required
def add_row_above(request, matrix_id, row_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	if matrix.owner_id == current_user.id:

		matrix = Matrix.objects.get(id=matrix_id)

		oldCells = Cell.objects.filter(matrix=matrix_id).filter(ycoordinate__gte=row_id)
		columns = Cell.objects.filter(matrix=matrix_id).values('xcoordinate').distinct()
		
		for oldcell in oldCells:
		
			oldcell.ycoordinate += 1
			oldcell.save()

		for i, column in enumerate(columns):

			cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=row_id)
			cell.save()


	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))

	
@login_required
def add_row_below(request, matrix_id, row_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	if matrix.owner_id == current_user.id:

		matrix = Matrix.objects.get(id=matrix_id)

		oldCells = Cell.objects.filter(matrix=matrix_id).filter(ycoordinate__gt=row_id)
		columns = Cell.objects.filter(matrix=matrix_id).values('xcoordinate').distinct()

		new_row_id = int(row_id) + 1
			
		for oldcell in oldCells:
		
			oldcell.ycoordinate += 1
			oldcell.save()

		for i, column in enumerate(columns):

			cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=new_row_id)
			cell.save()


	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))
		

@login_required
def delete_column(request, matrix_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	if matrix.owner_id == current_user.id:
	
		matrix = Matrix.objects.get(id=matrix_id)
	
		deleteColumn = Cell.objects.filter(matrix=matrix_id).values('xcoordinate').distinct().count()
		deleteColumn = deleteColumn - 1

		oldCells = Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn)
		
		for oldCell in oldCells:
		
			if oldCell.image is not None:
				
				image = Image.objects.get(id=oldCell.image.id)
				
				image.active = True
				
				image.save()
			
			if oldCell.blogpost != '':
			
				credential = Credential.objects.get(username=request.user.username)
	
				if credential != []:

					if credential.apppwd != '':
			
						response = delete_a_post_from_wordpress(request.user.username, oldCell.blogpost)

		Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn).delete()


	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))
	

@login_required
def delete_this_column(request, matrix_id, column_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	if matrix.owner_id == current_user.id:
	
		matrix = Matrix.objects.get(id=matrix_id)
	
		deleteColumn = int(column_id)

		oldCells = Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn)
	
		for oldCell in oldCells:
		
			oldCell.xcoordinate -= 1
			oldCell.save()
		
			if oldCell.image is not None:
				
				image = Image.objects.get(id=oldCell.image.id)
				
				image.active = True
				
				image.save()

			if oldCell.blogpost != '':

				credential = Credential.objects.get(username=request.user.username)
	
				if credential != []:

					if credential.apppwd != '':
			
						response = delete_a_post_from_wordpress(request.user.username, oldCell.blogpost)

		Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn).delete()
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)
	
	data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))
		

@login_required
def delete_row(request, matrix_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	if matrix.owner_id == current_user.id:
	
		matrix = Matrix.objects.get(id=matrix_id)
	
		deleteRow = Cell.objects.filter(matrix=matrix_id).values('ycoordinate').distinct().count()
		deleteRow = deleteRow -1

		oldCells = Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow)

		for oldCell in oldCells:
		
			if oldCell.image is not None:
				
				image = Image.objects.get(id=oldCell.image.id)
				
				image.active = True
				
				image.save()

			if oldCell.blogpost != '':

				credential = Credential.objects.get(username=request.user.username)
	
				if credential != []:

					if credential.apppwd != '':
			
						response = delete_a_post_from_wordpress(request.user.username, oldCell.blogpost)

		Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow).delete()


	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))


@login_required
def delete_this_row(request, matrix_id, row_id):

	current_user = request.user

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	
	if matrix.owner_id == current_user.id:

		matrix = Matrix.objects.get(id=matrix_id)
	
		deleteRow = int(row_id)

		oldCells = Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow)
	
		for oldCell in oldCells:
		
			oldCell.ycoordinate -= 1
			oldCell.save()

			if oldCell.image is not None:
				
				image = Image.objects.get(id=oldCell.image.id)
				
				image.active = True
				
				image.save()

			if oldCell.blogpost != '':

				credential = Credential.objects.get(username=request.user.username)
	
				if credential != []:

					if credential.apppwd != '':
			
						response = delete_a_post_from_wordpress(request.user.username, oldCell.blogpost)

		Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow).delete()
	
	matrix_list = Matrix.objects.all
	image_list = Image.objects.filter(owner=current_user).filter(active=True)
	server_list = Server.objects.all

	matrix_cells = generateMatrix(matrix_id)
	columns = generateColumns(matrix_id)
	rows = generateRows(matrix_id)

	data = { 'owner': owner, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'image_list': image_list, 'server_list': server_list }

	return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))
	
	
