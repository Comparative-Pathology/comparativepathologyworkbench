#!/usr/bin/python3
#
# ##
# \file         profile.py
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
# The (User) Profile Model - only Used to confirm email addresses
# ##
#
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from matrices.models import Collection


#
#   PROFILE
#
class Profile(models.Model):
    user = models.OneToOneField(User,
                                related_name='profile',
                                on_delete=models.CASCADE)
    bio = models.TextField(max_length=500,
                           blank=True)
    location = models.CharField(max_length=30,
                                blank=True)
    birth_date = models.DateField(null=True,
                                  blank=True)
    email_confirmed = models.BooleanField(default=False)
    active_collection = models.ForeignKey(Collection,
                                          related_name='active_collections',
                                          null=True,
                                          on_delete=models.DO_NOTHING)
    last_used_collection = models.ForeignKey(Collection,
                                             related_name='lastused_collections',
                                             null=True,
                                             on_delete=models.DO_NOTHING)
    hide_collection_image = models.BooleanField(default=False)

    @classmethod
    def create(cls, user, bio, location, birth_date, email_confirmed, active_collection, last_used_collection,
               hide_collection_image):
        return cls(user=user, bio=bio, location=location, birth_date=birth_date, email_confirmed=email_confirmed,
                   active_collection=active_collection, last_used_collection=last_used_collection,
                   hide_collection_image=hide_collection_image)

    def __str__(self):
        return f"{self.id}, {self.bio}, {self.location}, {self.birth_date}, {self.email_confirmed}, \
            {self.active_collection}, {self.last_used_collection}, {self.hide_collection_image}"

    def __repr__(self):
        return f"{self.id}, {self.user.id}, {self.bio}, {self.location}, {self.birth_date}, {self.email_confirmed}, \
            {self.active_collection}, {self.last_used_collection}, {self.hide_collection_image}"

    def set_active_collection(self, a_collection):
        self.active_collection = a_collection

    def set_last_used_collection(self, a_collection):
        self.last_used_collection = a_collection

    def set_hide_collection_image(self, a_hide_collection_image):
        self.a_hide_collection_image = a_hide_collection_image

    def has_active_collection(self):
        if self.active_collection is None:
            return False
        else:
            return True

    def has_last_used_collection(self):
        if self.last_used_collection is None:
            return False
        else:
            return True

    def is_hide_collection_image(self):
        if self.hide_collection_image is False:
            return False
        else:
            return True


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
