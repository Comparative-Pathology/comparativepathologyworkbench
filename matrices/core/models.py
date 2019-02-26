# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

# Create your models here.

class Matrix(models.Model):
	title = models.CharField(max_length=255, default='')
	description = models.TextField(max_length=4095, default='')
	blogpost = models.CharField(max_length=50, blank=True, default='')
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	height = models.IntegerField(default=75, blank=False)
	width = models.IntegerField(default=75, blank=False)
	owner = models.ForeignKey(User)
	
	def __str__(self):
		return '%s, %s, %s, %s, %s' % (self.id, self.title, self.description, self.blogpost, self.owner)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	location = models.CharField(max_length=30, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()


class Type(models.Model):
	name = models.CharField(max_length=12, blank=False, unique=True, default='')
	owner = models.ForeignKey(User)

	def __str__(self):
		#return '%s %s %s' % (self.id, self.name, self.owner)
		return '%s' % ( self.name )


class Protocol(models.Model):
	name = models.CharField(max_length=12, blank=False, unique=True, default='')
	owner = models.ForeignKey(User)

	def __str__(self):
		#return '%s %s %s' % (self.id, self.name, self.owner)
		return '%s' % ( self.name )


class Server(models.Model):
	name = models.CharField(max_length=50, blank=False, unique=True)
	url = models.CharField(max_length=50, blank=False, default='')
	uid = models.CharField(max_length=50, blank=True, default='')
	pwd = models.CharField(max_length=50, blank=True, default='')
	type = models.ForeignKey(Type, default=0, on_delete=models.CASCADE)
	owner = models.ForeignKey(User)
	
	def __str__(self):
		return '%s %s %s %s %s %s %s' % (self.id, self.name, self.url, self.uid, self.pwd, self.type, self.owner)


class Command(models.Model):
	name = models.CharField(max_length=50, unique=True, blank=False)
	application = models.CharField(max_length=25, blank=True, default='')
	preamble = models.CharField(max_length=50, blank=True, default='')
	postamble = models.CharField(max_length=50, blank=True, default='')
	protocol = models.ForeignKey(Protocol, default=0, on_delete=models.CASCADE)
	type = models.ForeignKey(Type, default=0, on_delete=models.CASCADE)
	owner = models.ForeignKey(User)

	def __str__(self):
		return '%s %s %s %s %s %s %s %s' % (self.id, self.name, self.application, self.preamble, self.postamble, self.protocol, self.type, self.owner)


class Image(models.Model):	
	identifier = models.IntegerField(default=0)
	name = models.CharField(max_length=255, blank=False, default='')
	server = models.ForeignKey(Server, default=0, on_delete=models.CASCADE)
	viewer_url = models.CharField(max_length=255, blank=False, default='')
	birdseye_url = models.CharField(max_length=255, blank=False, default='')
	owner = models.ForeignKey(User)
	active = models.BooleanField(default=True)
	roi = models.IntegerField(default=0)
	#cell = models.ForeignKey(Cell, null=True, on_delete=models.CASCADE)
	
	def __str__(self):
		return '%s %s %s %s %s %s %s %s' % (self.id, self.identifier, self.name, self.server, 
		self.viewer_url, self.birdseye_url, self.owner, self.active)
	

class Cell(models.Model):
	matrix = models.ForeignKey(Matrix, on_delete=models.CASCADE)
	title = models.CharField(max_length=255, default='')
	description = models.TextField(max_length=4095, default='')
	xcoordinate = models.IntegerField(default=0)
	ycoordinate = models.IntegerField(default=0)
	blogpost = models.CharField(max_length=50, blank=True, default='')
	image = models.ForeignKey(Image, null=True, on_delete=models.CASCADE)

	def __str__(self):
		return '%s %s %s %s %s %s %s %s' % (self.id, self.matrix, self.title, self.description, self.xcoordinate, self.ycoordinate, self.blogpost, self.image)


class Blog(models.Model):
	name = models.CharField(max_length=50, blank=False, unique=True)
	protocol = models.ForeignKey(Protocol, default=0, on_delete=models.CASCADE)
	url = models.CharField(max_length=50, blank=False, default='')
	application = models.CharField(max_length=25, blank=True, default='')
	preamble = models.CharField(max_length=50, blank=True, default='')
	postamble = models.CharField(max_length=50, blank=True, default='')
	owner = models.ForeignKey(User)
	
	def __str__(self):
		return '%s %s %s %s %s %s %s %s' % (self.id, self.name, self.protocol, self.url, self.application, self.preamble, self.postamble, self.owner)


class Credential(models.Model):
	username = models.CharField(max_length=50, blank=False, unique=True)
	wordpress = models.IntegerField(default=0, blank=False)
	apppwd = models.CharField(max_length=50, blank=True, default='')
	owner = models.ForeignKey(User)
	
	def __str__(self):
		return '%s %s %s %s %s' % (self.id, self.username, self.wordpress, self.apppwd, self.owner)


