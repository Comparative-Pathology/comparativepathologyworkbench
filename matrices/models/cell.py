#!/usr/bin/python3
###!
# \file         cell.py
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
# The Bench Cell Model.
###
from __future__ import unicode_literals

import json, urllib, requests, base64, hashlib, requests

from django.db import models
from django.db.models import Q
from django.db.models import Count
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.timezone import now
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from random import randint
from decouple import config


from matrices.models import Matrix
from matrices.models import Image


"""
    CELL (in a BENCH)
"""
class Cell(models.Model):
    matrix = models.ForeignKey(Matrix, related_name='bench_cells', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=4095, default='')
    xcoordinate = models.IntegerField(default=0)
    ycoordinate = models.IntegerField(default=0)
    blogpost = models.CharField(max_length=50, blank=True, default='')
    image = models.ForeignKey(Image, null=True, related_name='image', on_delete=models.DO_NOTHING)

    def set_matrix(self, a_matrix):
        self.matrix = a_matrix

    def set_title(self, a_title):
        self.title = a_title

    def set_description(self, a_description):
        self.description = a_description

    def set_xcoordinate(self, a_column):
        self.xcoordinate = a_column

    def set_ycoordinate(self, a_row):
        self.ycoordinate = a_row

    def set_blogpost(self, a_blogpost):
        self.blogpost = a_blogpost

    def set_image(self, an_image):
        self.image = an_image

    @classmethod
    def create(cls, matrix, title, description, xcoordinate, ycoordinate, blogpost, image):
        return cls(matrix=matrix, title=title, description=description, xcoordinate=xcoordinate, ycoordinate=ycoordinate, blogpost=blogpost, image=image)

    def __str__(self):
        str_image = ""

        if self.has_image():
            str_image = self.image.id
        else:
            str_image = "None"

        return f"{self.id}, {self.matrix.id}, {self.title}, {self.description}, {self.xcoordinate}, {self.ycoordinate}, {self.blogpost}, {str_image}"

    def __repr__(self):
        str_image = ""

        if self.has_image():
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

    def increment_x(self):
        self.xcoordinate += 1

    def increment_y(self):
        self.ycoordinate += 1

    def decrement_x(self):
        self.xcoordinate -= 1

    def decrement_y(self):
        self.ycoordinate -= 1
