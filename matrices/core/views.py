# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse

from django.template import loader

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect

from django.urls import reverse

from django.views import generic

from django import forms

from django.forms.models import inlineformset_factory

from django.contrib.auth import login

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site

from django.contrib import messages 

from django.utils.encoding import force_bytes
from django.utils.encoding import force_text

from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode

from django.template.loader import render_to_string

import requests

from decouple import config

from matrices.core.forms import SignUpForm
from matrices.core.tokens import account_activation_token

from matrices.core.forms import MatrixForm
from matrices.core.forms import NewMatrixForm
from matrices.core.forms import CellForm
from matrices.core.forms import HeaderForm
from matrices.core.forms import CommandForm
from matrices.core.forms import ServerForm
from matrices.core.forms import CommentForm
from matrices.core.forms import BlogForm
from matrices.core.forms import CredentialForm
from matrices.core.forms import ProtocolForm
from matrices.core.forms import TypeForm
from matrices.core.forms import AuthorityForm
from matrices.core.forms import AuthorisationForm
from matrices.core.forms import EditUserForm

from matrices.core.models import Matrix
from matrices.core.models import Cell
from matrices.core.models import Type
from matrices.core.models import Protocol
from matrices.core.models import Server
from matrices.core.models import Command
from matrices.core.models import Image
from matrices.core.models import Blog
from matrices.core.models import Credential
from matrices.core.models import Authority
from matrices.core.models import Authorisation

from matrices.core.routines import AESCipher

from matrices.core.models import authorisation_list_select_related_matrix_by_user
from matrices.core.models import authorisation_list_select_related_matrix
from matrices.core.models import matrix_list_by_user
from matrices.core.models import matrix_list_not_by_user
from matrices.core.models import matrix_list_all
from matrices.core.models import get_authority_for_matrix_and_user_and_requester
from matrices.core.models import credential_exists
from matrices.core.models import authorisation_exits_for_matrix_and_permitted
from matrices.core.models import get_primary_wordpress_server

from django.db.models import Q 


WORDPRESS_SUCCESS = 'Success!'

HTTP_POST = 'POST'


#
# HOME VIEW
#
def home(request):


	credential_flag = ''	
	
	if request.user.is_anonymous == True:

		matrix_list = list()
		my_matrix_list = list()

		image_list = []
		server_list = []
	
	else:
	
		if credential_exists(request.user) == True:

			credential_flag = request.user.username

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

	print("request.user : ", request.user)

	data = { 'credential_flag': credential_flag, 'my_matrix_list': my_matrix_list, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'home.html', data)


#
# ABOUT VIEW
#
def about(request):

	if request.user.is_anonymous == True:

		matrix_list = list()
		my_matrix_list = list()

		image_list = []
		server_list = []
	
	else:
	
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

	data = { 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'about/about.html', data)


#
# PEOPLE VIEW
#
def people(request):

	if request.user.is_anonymous == True:

		matrix_list = list()
		my_matrix_list = list()

		image_list = []
		server_list = []
	
	else:
	
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

	data = { 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'about/people.html', data)


#
# PEOPLE VIEW
#
def howto(request):

	if request.user.is_anonymous == True:

		matrix_list = list()
		my_matrix_list = list()

		image_list = []
		server_list = []
	
	else:
	
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

	data = { 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'about/howto.html', data)


#
# VIEWS FOR AUTHORIZATION
#
def signup(request):

	if request.method == HTTP_POST:

		form = SignUpForm(request.POST)

		if form.is_valid() == True:

			user = form.save(commit=False)

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

	else:

		return render(request, 'user/account_activation_invalid.html')


#
# VIEWS FOR HOSTS
#
@login_required
def list_image_cart(request):

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

	user = get_object_or_404(User, pk=request.user.id)

	credential_flag = ''	
	
	if credential_exists(user) == True:

		credential_flag = user.username

		data = { 'credential_flag': credential_flag, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/list_image_cart.html', data)

	else:

		data = { 'credential_flag': credential_flag, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/list_image_cart.html', data)
	

@login_required
def list_imaging_hosts(request):

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
	
	user = get_object_or_404(User, pk=request.user.id)

	credential_flag = ''	
	
	if credential_exists(user) == True:

		credential_flag = user.username

		data = { 'credential_flag': credential_flag, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/list_imaging_hosts.html', data)

	else:

		data = { 'credential_flag': credential_flag, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/list_imaging_hosts.html', data)
	

@login_required
def maintenance(request):

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

	type_list = Type.objects.all()
	protocol_list = Protocol.objects.all()
	command_list = Command.objects.all()
	user_list = User.objects.all()
	blog_list = Blog.objects.all()
	authority_list = Authority.objects.all()

	if request.user.is_superuser == True:

		data = { 'user_list': user_list, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'type_list': type_list, 'protocol_list': protocol_list, 'command_list': command_list, 'blog_list': blog_list, 'authority_list': authority_list }

		return render(request, 'host/maintenance.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	

@login_required
def authorisation(request):

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
	user_list = User.objects.all()
	credential_list = Credential.objects.all()

	if request.user.is_superuser == True:

		data = { 'user_list': user_list, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'credential_list': credential_list }

		return render(request, 'host/authorisation.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def view_user(request, user_id):

	subject = get_object_or_404(User, pk=user_id)
	user = get_object_or_404(User, pk=request.user.id)

	my_matrix_list = Matrix.objects.filter(owner=user)

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

	image_list = Image.objects.filter(owner=user).filter(active=True)
	server_list = Server.objects.all()

	data = { 'subject': subject, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
		
	return render(request, 'host/detail_user.html', data)


@login_required
def edit_user(request, user_id):

	subject = get_object_or_404(User, pk=user_id)
	user = get_object_or_404(User, pk=request.user.id)
		
	my_matrix_list = Matrix.objects.filter(owner=user)

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

	image_list = Image.objects.filter(owner=user).filter(active=True)
	server_list = Server.objects.all()

	if user.is_superuser == True:

		if request.method == HTTP_POST:
	
			form = EditUserForm(request.POST, instance=subject)
			
			if form.is_valid() == True:
			
				user = form.save(commit=False)
				
				user.save()
						
				return HttpResponseRedirect(reverse('matrices:authorisation', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'subject': subject, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = EditUserForm(instance=subject)
			
			data = { 'subject': subject, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/edit_user.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	
@login_required
def delete_user(request, user_id):

	subject = get_object_or_404(User, pk=user_id)
	
	if request.user.is_superuser == True:

		subject.delete()
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	return HttpResponseRedirect(reverse('matrices:authorisation', args=()))						


@login_required
def new_blog_command(request):

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

	if request.user.is_superuser == True:
	
		if request.method == HTTP_POST:
	
			form = BlogForm(request.POST)
		
			if form.is_valid() == True:
		
				blog = form.save(commit=False)

				blog.set_owner(request.user)

				blog.save()

				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))
		
			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = BlogForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/new_blog_command.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def view_blog_command(request, blog_id):

	blog = get_object_or_404(Blog, pk=blog_id)

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
	
	if request.user.is_superuser == True:
	
		data = { 'blog_id': blog_id, 'blog': blog, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/detail_blog_command.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def edit_blog_command(request, blog_id):

	blog = get_object_or_404(Blog, pk=blog_id)
	
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

	if request.user.is_superuser == True:

		if request.method == HTTP_POST:
	
			form = BlogForm(request.POST, instance=blog)
			
			if form.is_valid() == True:
			
				blog = form.save(commit=False)

				blog.set_owner(request.user)

				blog.save()
						
				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'blog': blog }
			
		else:
	
			form = BlogForm(instance=blog)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'blog': blog }

		return render(request, 'host/edit_blog_command.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def delete_blog_command(request, blog_id):

	blog = get_object_or_404(Blog, pk=blog_id)
	
	if request.user.is_superuser == True:

		blog.delete()
	
		return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def new_blog_credential(request):

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

	if request.user.is_superuser == True:
	
		if request.method == HTTP_POST:
	
			form = CredentialForm(request.POST)
		
			if form.is_valid() == True:
		
				credential = form.save(commit=False)

				credential.set_owner(request.user)

				credential.save()

				return HttpResponseRedirect(reverse('matrices:authorisation', args=()))
		
			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = CredentialForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/new_blog_credential.html', data)

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	
@login_required
def view_blog_credential(request, credential_id):

	credential = get_object_or_404(Credential, pk=credential_id)

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
	
	if request.user.is_superuser == True:

		data = { 'credential_id': credential_id, 'credential': credential, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/detail_blog_credential.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	

@login_required
def edit_blog_credential(request, credential_id):

	credential = get_object_or_404(Credential, pk=credential_id)
	
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

	if request.user.is_superuser == True:

		if request.method == HTTP_POST:
	
			form = CredentialForm(request.POST, instance=credential)
			
			if form.is_valid() == True:
			
				credential = form.save(commit=False)

				credential.set_owner(request.user)

				credential.save()
						
				return HttpResponseRedirect(reverse('matrices:authorisation', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'credential': credential }
			
		else:
	
			form = CredentialForm(instance=credential)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'credential': credential }

		return render(request, 'host/edit_blog_credential.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def delete_blog_credential(request, credential_id):

	credential = get_object_or_404(Credential, pk=credential_id)
	
	if request.user.is_superuser == True:

		credential.delete()
	
		return HttpResponseRedirect(reverse('matrices:authorisation', args=()))						

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def new_type(request):

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

	if request.user.is_superuser == True:
	
		if request.method == HTTP_POST:
		
			form = TypeForm(request.POST)
		
			if form.is_valid() == True:
		
				type = form.save(commit=False)

				type.set_owner(request.user)

				type.save()

				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						
		
			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = TypeForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/new_type.html', data)

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	
@login_required
def view_type(request, type_id):

	type = get_object_or_404(Type, pk=type_id)

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
	
	if request.user.is_superuser == True:
	
		data = { 'type_id': type_id, 'type': type, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/detail_type.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def edit_type(request, type_id):

	type = get_object_or_404(Type, pk=type_id)
	
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

	if request.user.is_superuser == True:

		if request.method == HTTP_POST:
	
			form = TypeForm(request.POST, instance=type)
			
			if form.is_valid() == True:
			
				type = form.save(commit=False)

				type.set_owner(request.user)

				type.save()
						
				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'type': type }
			
		else:
	
			form = TypeForm(instance=type)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'type': type }

		return render(request, 'host/edit_type.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def delete_type(request, type_id):

	type = get_object_or_404(Type, pk=type_id)
	
	if request.user.is_superuser == True:

		type.delete()
	
		return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def new_authority(request):

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

	if request.user.is_superuser == True:
	
		if request.method == HTTP_POST:
		
			form = AuthorityForm(request.POST)
		
			if form.is_valid() == True:
		
				authority = form.save(commit=False)

				authority.set_owner(request.user)

				authority.save()

				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						
		
			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = AuthorityForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/new_authority.html', data)

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	
@login_required
def view_authority(request, authority_id):

	authority = get_object_or_404(Authority, pk=authority_id)

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
	
	if request.user.is_superuser == True:
	
		data = { 'authority_id': authority_id, 'authority': authority, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/detail_authority.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def edit_authority(request, authority_id):

	authority = get_object_or_404(Authority, pk=authority_id)
	
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

	if request.user.is_superuser == True:

		if request.method == HTTP_POST:
	
			form = AuthorityForm(request.POST, instance=authority)
			
			if form.is_valid() == True:
			
				authority = form.save(commit=False)

				authority.set_owner(request.user)

				authority.save()
						
				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'authority': authority }
			
		else:
	
			form = AuthorityForm(instance=authority)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'authority': authority }

		return render(request, 'host/edit_authority.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def delete_authority(request, authority_id):

	authority = get_object_or_404(Authority, pk=authority_id)
	
	if request.user.is_superuser == True:

		authority.delete()
	
		return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def new_command(request):

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

	if request.user.is_superuser == True:
	
		if request.method == HTTP_POST:
	
			form = CommandForm(request.POST)
		
			if form.is_valid() == True:
		
				command = form.save(commit=False)

				command.set_owner(request.user)

				command.save()

				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))
		
			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = CommandForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/new_command.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	
@login_required
def view_command(request, command_id):

	command = get_object_or_404(Command, pk=command_id)

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
	
	if request.user.is_superuser == True:
	
		data = { 'command_id': command_id, 'command': command, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/detail_command.html', data)

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def edit_command(request, command_id):

	command = get_object_or_404(Command, pk=command_id)
	
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

	if request.user.is_superuser == True:

		if request.method == HTTP_POST:
	
			form = CommandForm(request.POST, instance=command)
			
			if form.is_valid() == True:
			
				command = form.save(commit=False)

				command.set_owner(request.user)

				command.save()
						
				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'command': command }
			
		else:
	
			form = CommandForm(instance=command)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'command': command }

		return render(request, 'host/edit_command.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def delete_command(request, command_id):

	command = get_object_or_404(Command, pk=command_id)
	
	if request.user.is_superuser == True:

		command.delete()
	
		return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def new_protocol(request):

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

	if request.user.is_superuser == True:
	
		if request.method == HTTP_POST:
	
			form = ProtocolForm(request.POST)
		
			if form.is_valid() == True:
		
				protocol = form.save(commit=False)

				protocol.set_owner(request.user)

				protocol.save()

				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						
		
			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = ProtocolForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/new_protocol.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	
@login_required
def view_protocol(request, protocol_id):

	protocol = get_object_or_404(Protocol, pk=protocol_id)

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
	
	if request.user.is_superuser == True:
	
		data = { 'protocol_id': protocol_id, 'protocol': protocol, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/detail_protocol.html', data)

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						
	

@login_required
def edit_protocol(request, protocol_id):

	protocol = get_object_or_404(Protocol, pk=protocol_id)
	
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

	if request.user.is_superuser == True:

		if request.method == HTTP_POST:
	
			form = ProtocolForm(request.POST, instance=protocol)
			
			if form.is_valid() == True:
			
				protocol = form.save(commit=False)

				protocol.set_owner(request.user)

				protocol.save()
				
				return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

			else:
			
				messages.error(request, "Error")
	
				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'protocol': protocol }
			
		else:
	
			form = ProtocolForm(instance=protocol)
			
			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'protocol': protocol }

		return render(request, 'host/edit_protocol.html', data)
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						



@login_required
def delete_protocol(request, protocol_id):

	protocol = get_object_or_404(Protocol, pk=protocol_id)
	
	if request.user.is_superuser == True:

		protocol.delete()
	
		return HttpResponseRedirect(reverse('matrices:maintenance', args=()))						

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def new_server(request):

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
	
	user = get_object_or_404(User, pk=request.user.id)
	
	credential_flag = ''	
	
	if credential_exists(user) == True:

		credential_flag = user.username

		if request.method == HTTP_POST:
	
			form = ServerForm(request.POST)
		
			if form.is_valid() == True:
		
				server = form.save(commit=False)

				server.set_owner(request.user)

				cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
				
				encryptedPwd = cipher.encrypt(server.pwd).decode()

				server.set_pwd(encryptedPwd)

				server.save()

				return HttpResponseRedirect(reverse('matrices:list_imaging_hosts', args=()))						

			else:

				messages.error(request, "Error")

				data = { 'credential_flag': credential_flag, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		else:

			form = ServerForm()

			data = { 'credential_flag': credential_flag, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/new_server.html', data)

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						
	
	
@login_required
def view_server(request, server_id):

	server = get_object_or_404(Server, pk=server_id)
	
	cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
	
	decryptedPwd = cipher.decrypt(server.pwd)

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
	
	owner = get_object_or_404(User, pk=server.owner_id)

	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		data = { 'owner': owner, 'server': server, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'host/detail_server.html', data)

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						
	

@login_required
def edit_server(request, server_id):

	server = get_object_or_404(Server, pk=server_id)
	
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

	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		if server.is_owned_by(request.user) == True or request.user.is_superuser == True:

			if request.method == HTTP_POST:
	
				form = ServerForm(request.POST, instance=server)
			
				if form.is_valid() == True:
			
					server = form.save(commit=False)

					cipher = AESCipher(config('EMAIL_HOST_PASSWORD'))
					
					encryptedPwd = cipher.encrypt(server.pwd).decode()

					server.set_pwd(encryptedPwd)
				
					server.set_owner(request.user)

					server.save()
				
					return HttpResponseRedirect(reverse('matrices:list_imaging_hosts', args=()))						

				else:
			
					messages.error(request, "Error")
	
					data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'server': server }
			
			else:
	
				form = ServerForm(instance=server)
			
				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'server': server }

			return render(request, 'host/edit_server.html', data)
	
		else:

			return HttpResponseRedirect(reverse('matrices:home', args=()))						

	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						



@login_required
def delete_server(request, server_id):

	server = get_object_or_404(Server, pk=server_id)
	
	if credential_exists(user) == True:

		if server.is_owned_by(request.user) == True or request.user.is_superuser == True:

			server.delete()
	
			return HttpResponseRedirect(reverse('matrices:list_imaging_hosts', args=()))						

		else:

			return HttpResponseRedirect(reverse('matrices:home', args=()))						
	
	else:

		return HttpResponseRedirect(reverse('matrices:home', args=()))						


#
# VIEWS FOR GALLERY
#
@login_required
def add_image(request, server_id, image_id, roi_id):

	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

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

		server = get_object_or_404(Server, pk=server_id)
	
		image_count = Image.objects.filter(identifier=image_id).filter(active=True).count()

		json_image = ''
		name = ''
		viewer_url = ''
		birdseye_url = ''

		if server.is_omero547() == True or server.is_omero56() == True:
	
			data = server.get_imaging_server_image_json(request, image_id)
	
			json_image = data['image']
			name = json_image['name']
			viewer_url = json_image['viewer_url']
			birdseye_url = json_image['birdseye_url']

		if server.is_wordpress() == True:

			data = server.get_wordpress_image_json(request, image_id)
	
			json_image = data['image']
			name = json_image['name']
			viewer_url = json_image['viewer_url']
			birdseye_url = json_image['thumbnail_url']

		if roi_id == '0':
		
			image = Image(identifier=image_id, name=name, server=server, viewer_url=viewer_url, birdseye_url=birdseye_url, owner=request.user, active=True, roi=0)
			
			image.save()
	
		else:
	
			json_rois = data['rois']
		
			for rois in json_rois:
		
				for shape in rois['shapes']:
			
					if shape['id'] == int(roi_id):
			
						viewer_url = shape['viewer_url']
						birdseye_url = shape['shape_url']
				
						image = Image(identifier=image_id, name=name, server=server, viewer_url=viewer_url, birdseye_url=birdseye_url, owner=request.user, active=True, roi=roi_id)

						image.save()
						
		if server.is_omero547() == True or server.is_omero56() == True:
	
			return HttpResponseRedirect(reverse('matrices:webgallery_show_image', args=(server_id, image_id)))				
	
		if server.is_wordpress() == True:

			return HttpResponseRedirect(reverse('matrices:webgallery_show_wordpress_image', args=(server_id, image_id)))				
	
	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def delete_image(request, image_id):

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

	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		image = get_object_or_404(Image, pk=image_id)
	
		image.delete()
					
		return HttpResponseRedirect(reverse('matrices:list_image_cart', args=()))				

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						
	

@login_required()
def show_ebi_server(request, server_id):
	"""
	Show the EBI Server
	"""

	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		server = get_object_or_404(Server, pk=server_id)
		
		if server.is_omero547() == True or server.is_omero56() == True:
		
			data = server.get_ebi_server_json(request)
		
			return render(request, 'ebi/show_server.html', data)
		
	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required()
def show_ebi_widget(request, server_id, experiment_id):
	"""
	Show the EBI widget
	"""

	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		server = get_object_or_404(Server, pk=server_id)
		
		if server.is_omero547() == True or server.is_omero56() == True:
		
			data = server.get_ebi_widget_json(request)
			
			gene = ''
			
			data.update({ 'experimentAccession': experiment_id, 'geneId': gene })
			
			return render(request, 'ebi/show_widget.html', data)
		
	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required()
def show_imaging_server(request, server_id):
	"""
	Show the Imaging Server
	"""

	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		server = get_object_or_404(Server, pk=server_id)
		
		if server.is_omero547() == True or server.is_omero56() == True:
		
			data = server.get_imaging_server_json(request)
		
			return render(request, 'gallery/show_server.html', data)
		
	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required()
def show_wordpress(request, server_id, page_id):
	"""
	Show the Wordpress Server
	"""

	user = get_object_or_404(User, pk=request.user.id)
	server = get_object_or_404(Server, pk=server_id)
	
	if credential_exists(user) == True:

		if server.is_wordpress() == True:
		
			data = server.get_wordpress_json(request, page_id)
		
			return render(request, 'gallery/show_wordpress.html', data)

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required()
def show_group(request, server_id, group_id):
	"""
	Show a group
	"""

	user = get_object_or_404(User, pk=request.user.id)
	server = get_object_or_404(Server, pk=server_id)
	
	if credential_exists(user) == True:

		data = server.get_imaging_server_group_json(request, group_id)
	
		return render(request, 'gallery/show_group.html', data)

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required()
def show_project(request, server_id, project_id):
	"""
	Show a project
	"""
	
	user = get_object_or_404(User, pk=request.user.id)
	server = get_object_or_404(Server, pk=server_id)
	
	if credential_exists(user) == True:

		data = server.get_imaging_server_project_json(request, project_id)

		return render(request, 'gallery/show_project.html', data)

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required()
def show_dataset(request, server_id, dataset_id):
	"""
	Show a dataset
	"""
	
	user = get_object_or_404(User, pk=request.user.id)
	server = get_object_or_404(Server, pk=server_id)
	
	if credential_exists(user) == True:

		data = server.get_imaging_server_dataset_json(request, dataset_id)
	
		return render(request, 'gallery/show_dataset.html', data)

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	
@login_required()
def show_image(request, server_id, image_id):
	"""
	Show an image
	"""
	
	user = get_object_or_404(User, pk=request.user.id)
	server = get_object_or_404(Server, pk=server_id)
	
	if credential_exists(user) == True:

		data = server.get_imaging_server_image_json(request, image_id)

		return render(request, 'gallery/show_image.html', data)

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required()
def show_wordpress_image(request, server_id, image_id):
	"""
	Show an image
	"""
	
	user = get_object_or_404(User, pk=request.user.id)	
	server = get_object_or_404(Server, pk=server_id)

	if credential_exists(user) == True:

		data = server.get_wordpress_image_json(request, image_id)

		return render(request, 'gallery/show_wordpress_image.html', data)

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


#
# VIEWS FOR ALL MY MATRICES
#
@login_required
def index_matrix(request):

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
	
	out_matrix_list = list()

	path = request.get_full_path()
	str1 = path.strip('/')
	str2 = str1.replace('matrices/', '')
	text_flag = ''
	
	if str2 == 'list_matrix':

		text_flag = " MY "

		out_matrix_list = matrix_list_by_user(request.user)

	else:

		text_flag = " ALL Permitted "
	
		if request.user.is_superuser == True:

			out_matrix_list = matrix_list_not_by_user(request.user)
	
		else:

			matrix_list_1 = matrix_list_by_user(request.user)
			matrix_list_2 = authorisation_list_select_related_matrix_by_user(request.user)
		
			out_matrix_list = matrix_list_1 + matrix_list_2

	
	user = get_object_or_404(User, pk=request.user.id)
	
	credential_flag = ''	
	
	if credential_exists(user) == True:

		credential_flag = user.username

		data = { 'text_flag': text_flag, 'credential_flag': credential_flag, 'out_matrix_list': out_matrix_list, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'matrices/index.html', data)

	else:
	
		data = { 'text_flag': text_flag, 'credential_flag': credential_flag, 'out_matrix_list': out_matrix_list, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'matrices/index.html', data)


@login_required
def matrix(request, matrix_id):

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


	matrix = get_object_or_404(Matrix, pk=matrix_id)
	owner = get_object_or_404(User, pk=matrix.owner_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	authority = get_authority_for_matrix_and_user_and_requester(matrix, user)

	if authority.is_none():
		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	
	credential_flag = ''	
	
	if credential_exists(user) == True:

		credential = Credential.objects.get(username=request.user.username)

		matrix_link = 'matrix_link'	
	
		if credential.has_apppwd() == False:

			matrix_link = ''

		matrix_cells = matrix.get_matrix()

		matrix_comments = matrix.get_matrix_comments()
		matrix_cells_comments = matrix.get_matrix_cell_comments()
		
		columns = matrix.get_columns()
		rows = matrix.get_rows()

		credential_flag = user.username

		data = { 'credential_flag': credential_flag, 'matrix_link': matrix_link, 'authority': authority, 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_cells_comments': matrix_cells_comments, 'matrix_comments': matrix_comments, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'matrices/matrix.html', data)

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						
	

@login_required
def new_matrix(request):

	user = get_object_or_404(User, pk=request.user.id)
	
	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

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

		if request.method == HTTP_POST:
	
			form = NewMatrixForm(request.POST)
		
			if form.is_valid() == True:
			
				matrix = form.save(commit=False)

				rows = form.cleaned_data['rows']
				columns = form.cleaned_data['columns']
				
				rows = rows + 1
				columns = columns + 1

				if rows == 1:
					rows = 2

				if columns == 1:
					columns = 2
				
				if rows > 10:
					rows = 2

				if columns > 10:
					columns = 2
				
				if matrix.is_not_high_enough() == True:
					matrix.set_minimum_height()
				
				if matrix.is_not_wide_enough() == True:
					matrix.set_minimum_width()
					
				if matrix.is_too_high() == True:
					matrix.set_maximum_height()
					
				if matrix.is_too_wide() == True:
					matrix.set_maximum_width()

				credential = Credential.objects.get(username=request.user.username)
	
				post_id = ''
			
				if credential.has_apppwd() == True:

					returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, matrix.title, matrix.description)
					
					if returned_blogpost['status'] == WORDPRESS_SUCCESS:
					
						post_id = returned_blogpost['id']

					else:
					
						messages.error(request, "WordPress Error - Contact System Administrator")
					

				matrix.set_blogpost(post_id)

				matrix.set_owner(request.user)

				matrix.save()

				x = 0 
				
				while x <= columns:
				
					y = 0
	
					while y <= rows:

						cell = Cell(matrix=matrix, title="", description="", xcoordinate=x, ycoordinate=y)

						cell.save()
						
						y = y + 1
					
					x = x + 1

				return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix.id,)))				

			else:
		
				messages.error(request, "Error")

				data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
		else:
	
			form = NewMatrixForm()

			data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'matrices/new_matrix.html', data)
		
	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	
@login_required
def view_matrix_blog(request, matrix_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

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
	
		matrix_cells = matrix.get_matrix()
		columns = matrix.get_columns()
		rows = matrix.get_rows()

		blogpost = serverWordpress.get_wordpress_post(matrix.blogpost)

		if blogpost['status'] != WORDPRESS_SUCCESS:
					
			messages.error(request, "WordPress Error - Contact System Administrator")

		comment_list = list()
	
		comment_list = serverWordpress.get_wordpress_post_comments(matrix.blogpost)
		
		for comment in comment_list:
		
			if comment['status'] != WORDPRESS_SUCCESS:
					
				messages.error(request, "WordPress Error - Contact System Administrator")
	
		if request.method == HTTP_POST:
	
			form = CommentForm(request.POST)
			
			if form.is_valid() == True:

				cd = form.cleaned_data
				
				comment = cd.get('comment')
				
				if comment != '':
				
					returned_comment = serverWordpress.post_wordpress_comment(request.user.username, matrix.blogpost, comment)
					
					if returned_comment['status'] != WORDPRESS_SUCCESS:
					
						messages.error(request, "WordPress Error - Contact System Administrator")
				
				return HttpResponseRedirect(reverse('matrices:detail_matrix_blog', args=(matrix_id,)))						

			else:
			
				messages.error(request, "Error")
	
		else:
	
			form = CommentForm()
	
		data = { 'form': form, 'matrix': matrix, 'blogpost': blogpost, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'comment_list': comment_list }

		return render(request, 'matrices/detail_matrix_blog.html', data)

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def view_matrix(request, matrix_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

		blogLinkPost = Blog.objects.get(name='LinkPost')

		link_post_url = blogLinkPost.protocol.name + '://' + serverWordpress.url + '/' + blogLinkPost.application + '/' + matrix.blogpost

		matrix_link = link_post_url
	
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
	
		matrix_cells = matrix.get_matrix()
		columns = matrix.get_columns()
		rows = matrix.get_rows()

		data = { 'matrix': matrix, 'matrix_link': matrix_link, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

		return render(request, 'matrices/detail_matrix.html', data)

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						
	

@login_required
def edit_matrix(request, matrix_id):

	user = get_object_or_404(User, pk=request.user.id)
	
	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

		matrix = get_object_or_404(Matrix, pk=matrix_id)
	
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

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:

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
	
			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()
					
			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))				

		else:

			if request.method == HTTP_POST:
	
				form = MatrixForm(request.POST, instance=matrix)
			
				if form.is_valid() == True:
			
					matrix = form.save(commit=False)
					
					if matrix.is_not_high_enough() == True:
						matrix.set_minimum_height()
					
					if matrix.is_not_wide_enough() == True:
						matrix.set_minimum_width()
					
					if matrix.is_too_high() == True:
						matrix.set_maximum_height()
					
					if matrix.is_too_wide() == True:
						matrix.set_maximum_width()
						
					post_id = ''
				
					if matrix.has_no_blogpost() == True:
				
						credential = Credential.objects.get(username=request.user.username)
	
						if credential.has_apppwd() == True:

							returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, matrix.title, matrix.description)

							if returned_blogpost['status'] == WORDPRESS_SUCCESS:
							
								post_id = returned_blogpost['id']

							else:
							
								messages.error(request, "WordPress Error - Contact System Administrator")
							
						matrix.set_blogpost(post_id)

					matrix.save()
				
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
					
					matrix_cells = matrix.get_matrix()
					columns = matrix.get_columns()
					rows = matrix.get_rows()
							
					data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
				
					return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))						

				else:
			
					messages.error(request, "Error")
	
					data = { 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

			else:
	
				form = MatrixForm(instance=matrix)
			
			return render(request, 'matrices/edit_matrix.html', {'form': form, 'matrix': matrix, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, })
	
	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def delete_matrix(request, matrix_id):

	user = get_object_or_404(User, pk=request.user.id)
	
	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

		matrix = get_object_or_404(Matrix, pk=matrix_id)
	
		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:

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
			
			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()
					
			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))
		
		else:

			oldCells = Cell.objects.filter(matrix=matrix_id)

			for oldCell in oldCells:
		
				if oldCell.has_image() == True:
				
					image = Image.objects.get(id=oldCell.image.id)
				
					image.set_active()
				
					image.save()

				if oldCell.has_blogpost() == True:
			
					credential = Credential.objects.get(username=request.user.username)
	
					if credential.has_apppwd() == True:

						response = serverWordpress.delete_wordpress_post(request.user.username, oldCell.blogpost)

						if response != WORDPRESS_SUCCESS:
					
							messages.error(request, "WordPress Error - Contact System Administrator")

			if matrix.has_blogpost() == True:

				credential = Credential.objects.get(username=request.user.username)
	
				if credential.has_apppwd() == True:

					response = serverWordpress.delete_wordpress_post(request.user.username, matrix.blogpost)

					if response != WORDPRESS_SUCCESS:
					
						messages.error(request, "WordPress Error - Contact System Administrator")

			matrix.delete()
	
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

			data = { 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
			return HttpResponseRedirect(reverse('matrices:index', args=()))

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def edit_cell(request, matrix_id, cell_id):

	cell = get_object_or_404(Cell, pk=cell_id)
	matrix = get_object_or_404(Matrix, pk=matrix_id)
	
	serverWordpress = get_primary_wordpress_server()

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
	
	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:
	
		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:

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
			
			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()
					
			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))

		else:
		
			if request.method == HTTP_POST:
	
				if cell.is_header() == True:

					form = HeaderForm(request.POST, instance=cell)

					if form.is_valid() == True:
						
						cell = form.save(commit=False)
				
						cell.set_matrix(matrix)
			
						cell.save()

						matrix.save()

					else:
			
						messages.error(request, "Error")
	
						data = { 'form': form, 'matrix': matrix, 'cell': cell, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
				
						return render(request, 'matrices/edit_cell.html', data)

				else:
			
					imageOld = Image.objects.none
					imageNew = Image.objects.none
					
					if cell.has_no_image() == True:
			
						form = CellForm(request.user.id, None, request.POST, instance=cell)
					
					else:

						form = CellForm(request.user.id, cell.image.id, request.POST, instance=cell)
						
						imageOld = Image.objects.get(pk=cell.image.id)
	
						imageOld.set_active()
				
						imageOld.save()

					if form.is_valid() == True:
						
						imageNew = get_object_or_404(Image, pk=cell.image.id)
				
						imageNew.set_inactive()
				
						imageNew.save()
						
						cell = form.save(commit=False)
				
						cell.set_matrix(matrix)
					
						post_id = ''
				
						if cell.has_no_blogpost() == True:
				
							credential = Credential.objects.get(username=request.user.username)
	
							if credential.has_apppwd() == True:

								returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, cell.title, cell.description)
								
								if returned_blogpost['status'] == WORDPRESS_SUCCESS:
								
									post_id = returned_blogpost['id']

								else:
								
									messages.error(request, "WordPress Error - Contact System Administrator")
								
							cell.set_blogpost(post_id)

						cell.save()

						matrix.save()

					else:
			
						messages.error(request, "Error")
	
						data = { 'form': form, 'matrix': matrix, 'cell': cell, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
				
						return render(request, 'matrices/edit_cell.html', data)
				
				matrix_cells = matrix.get_matrix()
				columns = matrix.get_columns()
				rows = matrix.get_rows()
			
				data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
				return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))				

			else:
	
				if cell.is_header() == True:

					form = HeaderForm(instance=cell)

				else:

					if cell.has_no_image() == True:
			
						form = CellForm(request.user.id, None, instance=cell)
					
					else:

						form = CellForm(request.user.id, cell.image.id, instance=cell)

			return render(request, 'matrices/edit_cell.html', {'form': form, 'matrix': matrix, 'cell': cell, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list })

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def view_cell(request, matrix_id, cell_id):
	
	cell = get_object_or_404(Cell, pk=cell_id)
	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	serverWordpress = get_primary_wordpress_server()	
	
	if credential_exists(user) == True:
	
		blogLinkPost = Blog.objects.get(name='LinkPost')

		link_post_url = blogLinkPost.protocol.name + '://' + serverWordpress.url + '/' + blogLinkPost.application + '/' + cell.blogpost

		cell_link = link_post_url
	
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
	
		return render(request, 'matrices/detail_cell.html', {'cell': cell, 'cell_link': cell_link, 'matrix': matrix, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list })

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def view_cell_blog(request, matrix_id, cell_id):
	
	cell = get_object_or_404(Cell, pk=cell_id)
	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)

	serverWordpress = get_primary_wordpress_server()	
	
	if credential_exists(user) == True:
	
		blogpost = serverWordpress.get_wordpress_post(cell.blogpost)

		if blogpost['status'] != WORDPRESS_SUCCESS:
					
			messages.error(request, "WordPress Error - Contact System Administrator")

		comment_list = list()
	
		comment_list = serverWordpress.get_wordpress_post_comments(cell.blogpost)
	
		for comment in comment_list:
		
			if comment['status'] != WORDPRESS_SUCCESS:
					
				messages.error(request, "WordPress Error - Contact System Administrator")

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
		
		if request.method == HTTP_POST:
	
			form = CommentForm(request.POST)
			
			if form.is_valid() == True:

				cd = form.cleaned_data
				
				comment = cd.get('comment')
				
				if comment != '':
				
					returned_comment = serverWordpress.post_wordpress_comment(request.user.username, cell.blogpost, comment)

					if returned_comment['status'] != WORDPRESS_SUCCESS:
					
						messages.error(request, "WordPress Error - Contact System Administrator")
				
				return HttpResponseRedirect(reverse('matrices:view_cell_blog', args=(matrix_id, cell_id)))						

			else:
			
				messages.error(request, "Error")
	
		else:
	
			form = CommentForm()

		data = { 'form': form, 'matrix_id': matrix_id, 'cell': cell, 'matrix': matrix, 'blogpost': blogpost, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'comment_list': comment_list }

		return render(request, 'matrices/detail_cell_blog.html', data)

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def add_cell(request, matrix_id):

	matrix = Matrix.objects.get(id=matrix_id)
	
	user = get_object_or_404(User, pk=request.user.id)

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:

			return HttpResponseRedirect(reverse('matrices:home', args=()))
		
		else:

			cell_list = Cell.objects.filter(matrix=matrix)
			
			if not cell_list:
			
				cell1 = Cell(matrix=matrix, title="", description="", xcoordinate=0, ycoordinate=0)
				cell2 = Cell(matrix=matrix, title="", description="", xcoordinate=0, ycoordinate=1)
				cell3 = Cell(matrix=matrix, title="", description="", xcoordinate=0, ycoordinate=2)
				cell4 = Cell(matrix=matrix, title="", description="", xcoordinate=1, ycoordinate=0)
				cell5 = Cell(matrix=matrix, title="", description="", xcoordinate=1, ycoordinate=1)
				cell6 = Cell(matrix=matrix, title="", description="", xcoordinate=1, ycoordinate=2)
				cell7 = Cell(matrix=matrix, title="", description="", xcoordinate=2, ycoordinate=0)
				cell8 = Cell(matrix=matrix, title="", description="", xcoordinate=2, ycoordinate=1)
				cell9 = Cell(matrix=matrix, title="", description="", xcoordinate=2, ycoordinate=2)

				cell1.save()
				cell2.save()
				cell3.save()
				cell4.save()
				cell5.save()
				cell6.save()
				cell7.save()
				cell8.save()
				cell9.save()
				
				matrix.save()

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

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()

			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						
	

@login_required
def add_column(request, matrix_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			return HttpResponseRedirect(reverse('matrices:home', args=()))						

		else:
		
			matrix = Matrix.objects.get(id=matrix_id)
	
			nextColumn = matrix.get_column_count()
			rows = matrix.get_rows()
	
			for i, row in enumerate(rows):

				cell = Cell(matrix=matrix, title="", description="", xcoordinate=nextColumn, ycoordinate=i)

				cell.save()

			matrix.save()


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

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()
					
			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))				

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						
	

@login_required
def add_column_left(request, matrix_id, column_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			return HttpResponseRedirect(reverse('matrices:home', args=()))						

		else:
		
			oldCells = Cell.objects.filter(matrix=matrix_id).filter(xcoordinate__gte=column_id)
			rows = matrix.get_rows()
	
			for oldcell in oldCells:
		
				oldcell.increment_x()
				
				oldcell.save()

			for i, row in enumerate(rows):

				cell = Cell(matrix=matrix, title="", description="", xcoordinate=column_id, ycoordinate=i)
				cell.save()

			matrix.save()


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

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()

			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						
	

@login_required
def add_column_right(request, matrix_id, column_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			return HttpResponseRedirect(reverse('matrices:home', args=()))						

		else:
		
			oldCells = Cell.objects.filter(matrix=matrix_id).filter(xcoordinate__gt=column_id)
			rows = matrix.get_rows()
	
			for oldcell in oldCells:
		
				oldcell.increment_x()

				oldcell.save()

			new_column_id = int(column_id) + 1
	
			for i, row in enumerate(rows):

				cell = Cell(matrix=matrix, title="", description="", xcoordinate=new_column_id, ycoordinate=i)
				cell.save()

			matrix.save()


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

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()

			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						
	

@login_required
def add_row(request, matrix_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			return HttpResponseRedirect(reverse('matrices:home', args=()))						

		else:
		
			matrix = Matrix.objects.get(id=matrix_id)
	
			nextRow = matrix.get_row_count()
			columns = matrix.get_columns()

			for i, column in enumerate(columns):

				cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=nextRow)
				cell.save()

			matrix.save()


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

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()
	
			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						
		

@login_required
def add_row_above(request, matrix_id, row_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			return HttpResponseRedirect(reverse('matrices:home', args=()))						

			matrix = Matrix.objects.get(id=matrix_id)

			oldCells = Cell.objects.filter(matrix=matrix_id).filter(ycoordinate__gte=row_id)
			columns = matrix.get_columns()
		
			for oldcell in oldCells:
		
				oldcell.increment_y()
				
				oldcell.save()

			for i, column in enumerate(columns):

				cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=row_id)
				cell.save()

			matrix.save()


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

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()

			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						

	
@login_required
def add_row_below(request, matrix_id, row_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			return HttpResponseRedirect(reverse('matrices:home', args=()))						

		else:
		
			matrix = Matrix.objects.get(id=matrix_id)
	
			oldCells = Cell.objects.filter(matrix=matrix_id).filter(ycoordinate__gt=row_id)
			columns = matrix.get_columns()

			new_row_id = int(row_id) + 1
			
			for oldcell in oldCells:
		
				oldcell.increment_y()

				oldcell.save()
	
			for i, column in enumerate(columns):

				cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=new_row_id)
				cell.save()

			matrix.save()


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

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()

			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))
		
	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def delete_column(request, matrix_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			return HttpResponseRedirect(reverse('matrices:home', args=()))						

			matrix = Matrix.objects.get(id=matrix_id)
	
			#deleteColumn = Cell.objects.filter(matrix=matrix_id).values('xcoordinate').distinct().count()
			deleteColumn = matrix.get_column_count()
			deleteColumn = deleteColumn - 1

			oldCells = Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn)
		
			for oldCell in oldCells:
		
				if oldCell.has_image() == True:
				
					image = Image.objects.get(id=oldCell.image.id)
				
					image.set_active()
				
					image.save()
			
				if oldCell.has_blogpost() == True:
			
					credential = Credential.objects.get(username=request.user.username)
	
					if credential.has_apppwd() == True:
			
						response = serverWordpress.delete_wordpress_post(request.user.username, oldCell.blogpost)

						if response != WORDPRESS_SUCCESS:
					
							messages.error(request, "WordPress Error - Contact System Administrator")

			Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn).delete()

			matrix.save()


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

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()

			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))
	
		else:
	
			return HttpResponseRedirect(reverse('matrices:home', args=()))						
	
	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required
def delete_this_column(request, matrix_id, column_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			return HttpResponseRedirect(reverse('matrices:home', args=()))						

		else:
		
			matrix = Matrix.objects.get(id=matrix_id)
	
			deleteColumn = int(column_id)
			
			oldCells = Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn)
	
			for oldCell in oldCells:
		
				if oldCell.has_image() == True:
				
					image = Image.objects.get(id=oldCell.image.id)
				
					image.set_active()
				
					image.save()

				if oldCell.has_blogpost() == True:

					credential = Credential.objects.get(username=request.user.username)
	
					if credential.has_apppwd() == True:
			
						response = serverWordpress.delete_wordpress_post(request.user.username, oldCell.blogpost)
	
						if response != WORDPRESS_SUCCESS:
					
							messages.error(request, "WordPress Error - Contact System Administrator")

			Cell.objects.filter(matrix=matrix_id, xcoordinate=deleteColumn).delete()
	
			moveCells = Cell.objects.filter(matrix=matrix_id, xcoordinate__gt=deleteColumn)

			for moveCell in moveCells:
		
				moveCell.decrement_x()

				moveCell.save()
			
			matrix.save()


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

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()
		
			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						
		

@login_required
def delete_row(request, matrix_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			return HttpResponseRedirect(reverse('matrices:home', args=()))						

		else:
		
			matrix = Matrix.objects.get(id=matrix_id)
	
			#deleteRow = Cell.objects.filter(matrix=matrix_id).values('ycoordinate').distinct().count()
			deleteRow = get_row_count()
			deleteRow = deleteRow -1

			oldCells = Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow)

			for oldCell in oldCells:
		
				if oldCell.has_image() == True:
				
					image = Image.objects.get(id=oldCell.image.id)
					
					image.set_active()
				
					image.save()

				if oldCell.has_blogpost() == True:

					credential = Credential.objects.get(username=request.user.username)
	
					if credential.has_apppwd() == True:
			
						response = serverWordpress.delete_wordpress_post(request.user.username, oldCell.blogpost)

						if response != WORDPRESS_SUCCESS:
					
							messages.error(request, "WordPress Error - Contact System Administrator")

			Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow).delete()

			matrix.save()


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

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()

			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						
		

@login_required
def delete_this_row(request, matrix_id, row_id):

	matrix = get_object_or_404(Matrix, pk=matrix_id)
	user = get_object_or_404(User, pk=request.user.id)
	
	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			return HttpResponseRedirect(reverse('matrices:home', args=()))						

		else:
		
			matrix = Matrix.objects.get(id=matrix_id)
	
			deleteRow = int(row_id)

			oldCells = Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow)
	
			for oldCell in oldCells:
		
				if oldCell.has_image() == True:
				
					image = Image.objects.get(id=oldCell.image.id)
				
					image.set_active()
					
					print("image : ", image)
				
					image.save()

				if oldCell.has_blogpost() == True:

					credential = Credential.objects.get(username=request.user.username)
	
					if credential.has_apppwd() == True:
			
						response = serverWordpress.delete_wordpress_post(request.user.username, oldCell.blogpost)

						if response != WORDPRESS_SUCCESS:
					
							messages.error(request, "WordPress Error - Contact System Administrator")

			Cell.objects.filter(matrix=matrix_id, ycoordinate=deleteRow).delete()
	
			matrix.save()


			moveCells = Cell.objects.filter(matrix=matrix_id, ycoordinate__gt=deleteRow)

			for moveCell in moveCells:
		
				moveCell.decrement_y()

				moveCell.save()
			
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

			matrix_cells = matrix.get_matrix()
			columns = matrix.get_columns()
			rows = matrix.get_rows()
	
			data = { 'matrix': matrix, 'rows': rows, 'columns': columns, 'matrix_cells': matrix_cells, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

			return HttpResponseRedirect(reverse('matrices:matrix', args=(matrix_id,)))

	else:
	
		return HttpResponseRedirect(reverse('matrices:home', args=()))						


@login_required()
def overwrite_cell(request):
	"""
	AJAX - Overwrite Cell - MOVE
	"""

	source = request.POST['source']
	target = request.POST['target']
	source_type = request.POST['source_type']

	source_cell = get_object_or_404(Cell, pk=source)
	target_cell = get_object_or_404(Cell, pk=target)
	
	matrix = source_cell.matrix
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	user = get_object_or_404(User, pk=request.user.id)

	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)
	
		else:

			if matrix.get_max_row() == target_cell.ycoordinate:

				nextRow = matrix.get_row_count()
				columns = matrix.get_columns()

				for i, column in enumerate(columns):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=nextRow)

					cell.save()

				matrix.save()

			if matrix.get_max_column() == target_cell.xcoordinate:
	
				nextColumn = matrix.get_column_count()
				rows = matrix.get_rows()
	
				for i, row in enumerate(rows):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=nextColumn, ycoordinate=i)

					cell.save()

				matrix.save()

			if target_cell.has_image() == True:
				
				image = Image.objects.get(id=target_cell.image.id)
				
				image.set_active()
				
				image.save()

			if target_cell.has_blogpost() == True:

				credential = Credential.objects.get(username=request.user.username)
	
				if credential.has_apppwd() == True:
			
					response = serverWordpress.delete_wordpress_post(request.user.username, target_cell.blogpost)

					if response != WORDPRESS_SUCCESS:
					
						messages.error(request, "WordPress Error - Contact System Administrator")


			source_xcoordinate = source_cell.xcoordinate
			source_ycoordinate = source_cell.ycoordinate

			target_xcoordinate = target_cell.xcoordinate
			target_ycoordinate = target_cell.ycoordinate
	
			source_cell.xcoordinate = target_xcoordinate
			source_cell.ycoordinate = target_ycoordinate

			target_cell.xcoordinate = source_xcoordinate
			target_cell.ycoordinate = source_ycoordinate

			target_cell.title = ""
			target_cell.description = ""

			target_cell.blogpost = ""
			target_cell.image = None
			
			source_cell.save()
			target_cell.save()

			data = {'failure': False,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)

	else:
	
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)


@login_required()
def overwrite_cell_leave(request):
	"""
	AJAX - Overwrite Cell
	"""

	source = request.POST['source']
	target = request.POST['target']
	source_type = request.POST['source_type']
	
	source_cell = get_object_or_404(Cell, pk=source)
	target_cell = get_object_or_404(Cell, pk=target)
	
	matrix = source_cell.matrix
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	user = get_object_or_404(User, pk=request.user.id)

	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)
	
		else:

			if matrix.get_max_row() == target_cell.ycoordinate:

				nextRow = matrix.get_row_count()
				columns = matrix.get_columns()

				for i, column in enumerate(columns):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=nextRow)

					cell.save()

				matrix.save()

			if matrix.get_max_column() == target_cell.xcoordinate:
	
				nextColumn = matrix.get_column_count()
				rows = matrix.get_rows()
	
				for i, row in enumerate(rows):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=nextColumn, ycoordinate=i)

					cell.save()

				matrix.save()

			if target_cell.has_image() == True:
				
				image = Image.objects.get(id=target_cell.image.id)
				
				image.set_active()
				
				image.save()

			if target_cell.has_blogpost() == True:

				credential = Credential.objects.get(username=request.user.username)
	
				if credential.has_apppwd() == True:
			
					response = serverWordpress.delete_wordpress_post(request.user.username, target_cell.blogpost)

					if response != WORDPRESS_SUCCESS:
					
						messages.error(request, "WordPress Error - Contact System Administrator")

			target_cell.title = source_cell.title
			target_cell.description = source_cell.description
			
			if source_cell.has_image() == True:
			
				imageOld = Image.objects.get(pk=source_cell.image.id)

				imageNew = Image(identifier=imageOld.identifier, name=imageOld.name, server=imageOld.server, viewer_url=imageOld.viewer_url, birdseye_url=imageOld.birdseye_url, owner=imageOld.owner, active=imageOld.active, roi=imageOld.roi)
	
				imageNew.set_inactive()
				
				imageNew.save()
				
				target_cell.image = imageNew

			
			target_cell.blogpost = source_cell.blogpost

			if source_cell.has_blogpost() == True:
				
				credential = Credential.objects.get(username=request.user.username)
	
				post_id = ''

				if credential.has_apppwd() == True:

					returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, source_cell.title, source_cell.description)
								
					if returned_blogpost['status'] == WORDPRESS_SUCCESS:
								
						post_id = returned_blogpost['id']

					else:
								
						messages.error(request, "WordPress Error - Contact System Administrator")
							
				source_cell.set_blogpost(post_id)


			source_cell.save()
			target_cell.save()

			data = {'failure': False,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)

	else:
	
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)


@login_required()
def swap_cells(request):
	"""
	AJAX - Swap Cells
	"""

	source = request.POST['source']
	target = request.POST['target']
	source_type = request.POST['source_type']
	
	source_cell = get_object_or_404(Cell, pk=source)
	target_cell = get_object_or_404(Cell, pk=target)
	
	matrix = source_cell.matrix
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	user = get_object_or_404(User, pk=request.user.id)

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)
	
		else:

			if matrix.get_max_row() == target_cell.ycoordinate:

				nextRow = matrix.get_row_count()
				columns = matrix.get_columns()

				for i, column in enumerate(columns):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=nextRow)
					cell.save()

				matrix.save()

			if matrix.get_max_column() == target_cell.xcoordinate:
	
				nextColumn = matrix.get_column_count()
				rows = matrix.get_rows()
	
				for i, row in enumerate(rows):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=nextColumn, ycoordinate=i)

					cell.save()

				matrix.save()


			source_xcoordinate = source_cell.xcoordinate
			source_ycoordinate = source_cell.ycoordinate

			target_xcoordinate = target_cell.xcoordinate
			target_ycoordinate = target_cell.ycoordinate
	
			source_cell.xcoordinate = target_xcoordinate
			source_cell.ycoordinate = target_ycoordinate

			target_cell.xcoordinate = source_xcoordinate
			target_cell.ycoordinate = source_ycoordinate

			source_cell.save()
			target_cell.save()


			data = {'failure': False,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)

	else:
	
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)


@login_required()
def import_image(request):
	"""
	AJAX - Import Image
	"""

	source = request.POST['source']
	target = request.POST['target']
	source_type = request.POST['source_type']
	
	source_image = get_object_or_404(Image, pk=source)
	target_cell = get_object_or_404(Cell, pk=target)
	
	matrix = target_cell.matrix
	
	owner = get_object_or_404(User, pk=matrix.owner_id)
	user = get_object_or_404(User, pk=request.user.id)

	serverWordpress = get_primary_wordpress_server()

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)
	
		else:

			if matrix.get_max_row() == target_cell.ycoordinate:

				nextRow = matrix.get_row_count()
				columns = matrix.get_columns()

				for i, column in enumerate(columns):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=nextRow)
					cell.save()

				matrix.save()

			if matrix.get_max_column() == target_cell.xcoordinate:
	
				nextColumn = matrix.get_column_count()
				rows = matrix.get_rows()
	
				for i, row in enumerate(rows):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=nextColumn, ycoordinate=i)

					cell.save()

				matrix.save()

			if target_cell.has_image() == True:
			
				imageOld = Image.objects.get(pk=target_cell.image.id)
	
				imageOld.set_active()
				
				imageOld.save()

			source_image.set_inactive()
			
			source_image.save()
						
			post_id = ''
				
			target_cell.title = source_image.name
			target_cell.description = source_image.name
			
			target_cell.image = source_image
			
			if target_cell.has_no_blogpost() == True:
				
				credential = Credential.objects.get(username=request.user.username)
	
				if credential.has_apppwd() == True:

					returned_blogpost = serverWordpress.post_wordpress_post(request.user.username, target_cell.title, target_cell.description)
								
					if returned_blogpost['status'] == WORDPRESS_SUCCESS:
								
						post_id = returned_blogpost['id']

					else:
								
						messages.error(request, "WordPress Error - Contact System Administrator")
								
				target_cell.set_blogpost(post_id)

			target_cell.save()


			data = {'failure': False,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)

	else:
	
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)


@login_required()
def swap_rows(request):
	"""
	AJAX - Swap Rows
	"""

	source = request.POST['source']
	target = request.POST['target']
		
	in_source_cell = get_object_or_404(Cell, pk=source)
	in_target_cell = get_object_or_404(Cell, pk=target)
	
	matrix = in_source_cell.matrix

	owner = get_object_or_404(User, pk=matrix.owner_id)
	user = get_object_or_404(User, pk=request.user.id)

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)
	
		else:

			source_row_cells = matrix.get_row(in_source_cell.ycoordinate)
			target_row_cells = matrix.get_row(in_target_cell.ycoordinate)
	
			source_ycoordinate = in_source_cell.ycoordinate
			target_ycoordinate = in_target_cell.ycoordinate
	
			output_cells = list()
	
			for target_cell in target_row_cells:
	
				target_cell.set_ycoordinate(source_ycoordinate)
	
				output_cells.append(target_cell)
	
			for source_cell in source_row_cells:
	
				source_cell.set_ycoordinate(target_ycoordinate)
	
				output_cells.append(source_cell)

			for output_cell in output_cells:

				output_cell.save()
		

			if matrix.get_max_row() == in_target_cell.ycoordinate:

				nextRow = matrix.get_row_count()
				columns = matrix.get_columns()

				for i, column in enumerate(columns):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=nextRow)
					cell.save()

				matrix.save()

	
			data = {'failure': False,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)

	else:
	
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)


@login_required()
def swap_columns(request):
	"""
	AJAX - Swap Columns
	"""

	source = request.POST['source']
	target = request.POST['target']
		
	in_source_cell = get_object_or_404(Cell, pk=source)
	in_target_cell = get_object_or_404(Cell, pk=target)
	
	matrix = in_source_cell.matrix

	owner = get_object_or_404(User, pk=matrix.owner_id)
	user = get_object_or_404(User, pk=request.user.id)

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)
	
		else:

			source_column_cells = matrix.get_column(in_source_cell.xcoordinate)
			target_column_cells = matrix.get_column(in_target_cell.xcoordinate)
	
			source_xcoordinate = in_source_cell.xcoordinate
			target_xcoordinate = in_target_cell.xcoordinate
	
			output_cells = list()
	
			for target_cell in target_column_cells:
	
				target_cell.set_xcoordinate(source_xcoordinate)
	
				output_cells.append(target_cell)
	
			for source_cell in source_column_cells:
	
				source_cell.set_xcoordinate(target_xcoordinate)
	
				output_cells.append(source_cell)

			for output_cell in output_cells:

				output_cell.save()
	

			if matrix.get_max_column() == in_target_cell.xcoordinate:
	
				nextColumn = matrix.get_column_count()
				rows = matrix.get_rows()
	
				for i, row in enumerate(rows):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=nextColumn, ycoordinate=i)

					cell.save()

				matrix.save()

	
			data = {'failure': False,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)	

	else:
	
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)


@login_required()
def shuffle_columns(request):
	"""
	AJAX - Shuffle Columns
	"""

	source = request.POST['source']
	target = request.POST['target']
		
	in_source_cell = get_object_or_404(Cell, pk=source)
	in_target_cell = get_object_or_404(Cell, pk=target)
	
	source_xcoordinate = in_source_cell.xcoordinate
	target_xcoordinate = in_target_cell.xcoordinate
	
	matrix = in_source_cell.matrix

	owner = get_object_or_404(User, pk=matrix.owner_id)
	user = get_object_or_404(User, pk=request.user.id)

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)
	
		else:

			source_column_cells = matrix.get_column(source_xcoordinate)

			if source_xcoordinate < target_xcoordinate:
			
				oldCells = Cell.objects.filter(matrix=matrix.id).filter(xcoordinate__gt=source_xcoordinate).filter(xcoordinate__lte=target_xcoordinate)

				output_cells = list()
	
				for oldcell in oldCells:
		
					oldcell.decrement_x()
				
					output_cells.append(oldcell)
				
				for source_cell in source_column_cells:
	
					source_cell.set_xcoordinate(target_xcoordinate)
	
					output_cells.append(source_cell)
			
				for output_cell in output_cells:
			
					output_cell.save()


			if source_xcoordinate > target_xcoordinate:

				oldCells = Cell.objects.filter(matrix=matrix.id).filter(xcoordinate__gte=target_xcoordinate).filter(xcoordinate__lt=source_xcoordinate)

				output_cells = list()
	
				for oldcell in oldCells:
		
					oldcell.increment_x()
				
					output_cells.append(oldcell)
				
				for source_cell in source_column_cells:
	
					source_cell.set_xcoordinate(target_xcoordinate)
	
					output_cells.append(source_cell)
			
				for output_cell in output_cells:
			
					output_cell.save()


			if matrix.get_max_column() == target_xcoordinate:
	
				nextColumn = matrix.get_column_count()
				rows = matrix.get_rows()
	
				for i, row in enumerate(rows):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=nextColumn, ycoordinate=i)

					cell.save()

				matrix.save()

	
			data = {'failure': False,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)	
	
	else:
	
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)


@login_required()
def shuffle_rows(request):
	"""
	AJAX - Shuffle the Rows
	"""

	source = request.POST['source']
	target = request.POST['target']
		
	in_source_cell = get_object_or_404(Cell, pk=source)
	in_target_cell = get_object_or_404(Cell, pk=target)
	
	source_ycoordinate = in_source_cell.ycoordinate
	target_ycoordinate = in_target_cell.ycoordinate

	matrix = in_source_cell.matrix

	owner = get_object_or_404(User, pk=matrix.owner_id)
	user = get_object_or_404(User, pk=request.user.id)

	if credential_exists(user) == True:

		authority = get_authority_for_matrix_and_user_and_requester(matrix, request.user)

		if authority.is_viewer == True or authority.is_none == True:
		
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)
	
		else:

			source_row_cells = matrix.get_row(source_ycoordinate)
			
			if source_ycoordinate < target_ycoordinate:
			
				oldCells = Cell.objects.filter(matrix=matrix.id).filter(ycoordinate__gt=source_ycoordinate).filter(ycoordinate__lte=target_ycoordinate)

				output_cells = list()
	
				for oldcell in oldCells:
		
					oldcell.decrement_y()
				
					output_cells.append(oldcell)
				
				for source_cell in source_row_cells:
	
					source_cell.set_ycoordinate(target_ycoordinate)
	
					output_cells.append(source_cell)
			
				for output_cell in output_cells:
			
					output_cell.save()


			if source_ycoordinate > target_ycoordinate:

				oldCells = Cell.objects.filter(matrix=matrix.id).filter(ycoordinate__gte=target_ycoordinate).filter(ycoordinate__lt=source_ycoordinate)

				output_cells = list()
	
				for oldcell in oldCells:
		
					oldcell.increment_y()
				
					output_cells.append(oldcell)
				
				for source_cell in source_row_cells:
	
					source_cell.set_ycoordinate(target_ycoordinate)
	
					output_cells.append(source_cell)
			
				for output_cell in output_cells:
			
					output_cell.save()


			if matrix.get_max_row() == target_ycoordinate:

				nextRow = matrix.get_row_count()
				columns = matrix.get_columns()

				for i, column in enumerate(columns):

					cell = Cell(matrix=matrix, title="", description="", xcoordinate=i, ycoordinate=nextRow)
					cell.save()

				matrix.save()

	
			data = {'failure': False,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)
	
	else:
	
			data = {'failure': True,
					'source': str(source),
					'target': str(target)
			}
	
			return JsonResponse(data)


@login_required
def list_authorisation(request):

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

	server_list = Server.objects.all()
	image_list = Image.objects.filter(owner=request.user).filter(active=True)

	authorisation_list = Authorisation.objects.all()

	text_flag = ' ALL Permissions, ALL Benches'
	matrix_id = ''
	
	data = { 'matrix_id': matrix_id, 'text_flag': text_flag, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'authorisation_list': authorisation_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/list_authorisation.html', data)
	

@login_required
def list_my_authorisation(request):

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

	server_list = Server.objects.all()
	image_list = Image.objects.filter(owner=request.user).filter(active=True)

	authorisation_list = Authorisation.objects.filter(matrix__owner=request.user)

	text_flag = ' YOUR Permissions'	
	matrix_id = ''

	data = { 'matrix_id': matrix_id, 'text_flag': text_flag, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'authorisation_list': authorisation_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/list_authorisation.html', data)
	

@login_required
def list_bench_authorisation(request, matrix_id):

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

	server_list = Server.objects.all()
	image_list = Image.objects.filter(owner=request.user).filter(active=True)

	authorisation_list = Authorisation.objects.filter(matrix__id=matrix_id)

	text_flag = "CPW:" + format(int(matrix_id), '06d') + " Permissions"

	data = { 'matrix_id': matrix_id, 'text_flag': text_flag, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'authorisation_list': authorisation_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/list_authorisation.html', data)
	

@login_required
def list_my_bench_authorisation(request, matrix_id, user_id):

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

	server_list = Server.objects.all()
	image_list = Image.objects.filter(owner=request.user).filter(active=True)

	authorisation_list = Authorisation.objects.filter(matrix__owner=user_id).filter(matrix__id=matrix_id)

	user = get_object_or_404(User, pk=user_id)

	text_flag = "CPW:" + format(int(matrix_id), '06d') + " Permissions for User " + user.username

	data = { 'matrix_id': matrix_id, 'user_id': user_id, 'text_flag': text_flag, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'authorisation_list': authorisation_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/list_authorisation.html', data)
	

@login_required
def list_user_bench_authorisation(request, user_id):

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

	server_list = Server.objects.all()
	image_list = Image.objects.filter(owner=request.user).filter(active=True)

	authorisation_list = Authorisation.objects.filter(matrix__owner=user_id)

	user = get_object_or_404(User, pk=user_id)

	text_flag = " ALL Permissions for " + user.username
	matrix_id = ''

	data = { 'matrix_id': matrix_id, 'user_id': user_id, 'text_flag': text_flag, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'authorisation_list': authorisation_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/list_authorisation.html', data)
	

@login_required
def view_authorisation(request, authorisation_id):

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
	
	authorisation = get_object_or_404(Authorisation, pk=authorisation_id)

	data = { 'authorisation_id': authorisation_id, 'authorisation': authorisation, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/detail_authorisation.html', data)


@login_required
def new_authorisation(request):

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

	if request.method == HTTP_POST:
		
		next_page = request.POST.get('next', '/')

		form = AuthorisationForm(request.POST)

		if form.is_valid() == True:
		
			authorisation = form.save(commit=False)
			
			if authorisation_exits_for_matrix_and_permitted(authorisation.matrix, authorisation.permitted):
			
				authorisation_old = Authorisation.objects.get(Q(matrix=authorisation.matrix) & Q(permitted=authorisation.permitted))
				
				if authorisation_old.authority != authorisation.authority:
				
					authorisation_old.authority = authorisation.authority
					
					authorisation_old.save()

			else:
			
				authorisation.save()

			return HttpResponseRedirect(next_page)						
		
		else:
		
			text_flag = ''

			messages.error(request, "Error")

			data = { 'text_flag': text_flag, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
	else:
	
		text_flag = ''

		form = AuthorisationForm()

		form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.filter(owner=request.user))

		form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))

		data = { 'text_flag': text_flag, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/new_authorisation.html', data)

	
@login_required
def new_matrix_authorisation(request, matrix_id):

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

	if request.method == HTTP_POST:
		
		next_page = request.POST.get('next', '/')

		form = AuthorisationForm(request.POST)

		if form.is_valid() == True:
		
			authorisation = form.save(commit=False)
			
			if authorisation_exits_for_matrix_and_permitted(authorisation.matrix, authorisation.permitted):
			
				authorisation_old = Authorisation.objects.get(Q(matrix=authorisation.matrix) & Q(permitted=authorisation.permitted))
				
				if authorisation_old.authority != authorisation.authority:
				
					authorisation_old.authority = authorisation.authority
					
					authorisation_old.save()

			else:
			
				authorisation.save()

			return HttpResponseRedirect(next_page)						
		
		else:
		
			messages.error(request, "Error")

			text_flag = " for Bench CPW:" + format(int(matrix_id), '06d')
	
			data = { 'text_flag': text_flag, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }
			
	else:
	
		text_flag = " for Bench CPW:" + format(int(matrix_id), '06d')
	
		form = AuthorisationForm()

		form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.filter(id=matrix_id))

		form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))

		data = { 'text_flag': text_flag, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list }

	return render(request, 'host/new_authorisation.html', data)


@login_required
def edit_authorisation(request, authorisation_id):

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

	authorisation = get_object_or_404(Authorisation, pk=authorisation_id)
	
	if request.method == HTTP_POST:
	
		next_page = request.POST.get('next', '/')
		
		form = AuthorisationForm(request.POST, instance=authorisation)
			
		if form.is_valid() == True:
			
			authorisation = form.save(commit=False)

			if authorisation_exits_for_matrix_and_permitted(authorisation.matrix, authorisation.permitted):
			
				authorisation_old = Authorisation.objects.get(Q(matrix=authorisation.matrix) & Q(permitted=authorisation.permitted))
				
				if authorisation_old.authority != authorisation.authority:
				
					authorisation_old.authority = authorisation.authority
					
					authorisation_old.save()

			else:
			
				authorisation.save()

			return HttpResponseRedirect(next_page)						

		else:
			
			text_flag = ''
	
			messages.error(request, "Error")
	
			data = { 'text_flag': text_flag, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'authorisation': authorisation }
			
	else:
	
		text_flag = ''
		
		form = AuthorisationForm(instance=authorisation)

		form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))
			
		data = { 'text_flag': text_flag, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'authorisation': authorisation }

	return render(request, 'host/edit_authorisation.html', data)


@login_required
def edit_matrix_authorisation(request, matrix_id, authorisation_id):

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

	authorisation = get_object_or_404(Authorisation, pk=authorisation_id)
	
	if request.method == HTTP_POST:
	
		next_page = request.POST.get('next', '/')
		
		form = AuthorisationForm(request.POST, instance=authorisation)
			
		if form.is_valid() == True:
			
			authorisation = form.save(commit=False)

			if authorisation_exits_for_matrix_and_permitted(authorisation.matrix, authorisation.permitted):
			
				authorisation_old = Authorisation.objects.get(Q(matrix=authorisation.matrix) & Q(permitted=authorisation.permitted))
				
				if authorisation_old.authority != authorisation.authority:
				
					authorisation_old.authority = authorisation.authority
					
					authorisation_old.save()

			else:
			
				authorisation.save()

			return HttpResponseRedirect(next_page)						

		else:
			
			text_flag = " for Bench CPW:" + format(int(matrix_id), '06d')
	
			messages.error(request, "Error")
	
			data = { 'text_flag': text_flag, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'authorisation': authorisation }
			
	else:
	
		text_flag = " for Bench CPW:" + format(int(matrix_id), '06d')
	
		form = AuthorisationForm(instance=authorisation)

		form.fields['matrix'] = forms.ModelChoiceField(Matrix.objects.filter(id=matrix_id))

		form.fields['permitted'] = forms.ModelChoiceField(User.objects.exclude(id=request.user.id).exclude(is_superuser=True))
			
		data = { 'text_flag': text_flag, 'form': form, 'matrix_list': matrix_list, 'my_matrix_list': my_matrix_list, 'image_list': image_list, 'server_list': server_list, 'authorisation': authorisation }

	return render(request, 'host/edit_authorisation.html', data)


@login_required
#def delete_authorisation(request, authorisation_id, return_id):
def delete_authorisation(request, authorisation_id):

	authorisation = get_object_or_404(Authorisation, pk=authorisation_id)
	
	authorisation.delete()
	
	return HttpResponseRedirect(reverse('matrices:list_authorisation', args=()))						

