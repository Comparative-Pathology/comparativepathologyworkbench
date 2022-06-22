#!/usr/bin/python3
###!
# \file         matrix.py
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
# The Matrix Model - a Matrix is a Bench!
###
from __future__ import unicode_literals

import json, urllib, requests, base64, hashlib, requests

from django.db import models
from django.db.models import Q
from django.db.models import Count
from django.db.models.signals import post_save
from django.apps import apps
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.timezone import now
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from random import randint
from decouple import config

from requests.exceptions import HTTPError

from matrices.models import Collection

from matrices.routines import get_a_post_comments_from_wordpress


WORDPRESS_SUCCESS = 'Success!'


"""
    MATRIX (BENCH)
"""
class Matrix(models.Model):
    title = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=4095, default='')
    blogpost = models.CharField(max_length=50, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    height = models.IntegerField(default=75, blank=False)
    width = models.IntegerField(default=75, blank=False)
    owner = models.ForeignKey(User, related_name='matrices', on_delete=models.DO_NOTHING)
    last_used_collection = models.ForeignKey(Collection, related_name='collections', null=True, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Bench'
        verbose_name_plural = 'Benches'

    @classmethod
    def create(cls, title, description, blogpost, height, width, owner):
        return cls(title=title, description=description, blogpost=blogpost, height=height, width=width, owner=owner)

    def __str__(self):
        str_last_used_collection = ""

        if self.has_last_used_collection():
            str_last_used_collection = str(self.last_used_collection.id)
        else:
            str_last_used_collection = "No Collection"

        return f"CPW:{self.id:06d}, {self.title}"

    def __repr__(self):
        str_last_used_collection = ""

        if self.has_last_used_collection():
            str_last_used_collection = str(self.last_used_collection.id)
        else:
            str_last_used_collection = "No Collection"

        return f"{self.id}, {self.title}, {self.description}, {self.blogpost}, {self.created}, {self.modified}, {self.height}, {self.width}, {self.owner.id}, {str_last_used_collection}"

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

    def set_last_used_collection(self, a_last_used_collection):
        self.last_used_collection = a_last_used_collection

    def set_no_last_used_collection(self):
        self.last_used_collection = None

    def has_no_last_used_collection(self):
        if self.last_used_collection is None:
            return True
        else:
            return False

    def has_last_used_collection(self):
        if self.last_used_collection is None:
            return False
        else:
            return True

    def get_matrix(self):

        Cell = apps.get_model('matrices', 'Cell')

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

        Cell = apps.get_model('matrices', 'Cell')

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

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).values('ycoordinate').distinct()


    def get_row(self, a_row):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).filter(ycoordinate=a_row)


    def get_columns(self):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).values('xcoordinate').distinct()


    def get_column(self, a_column):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).filter(xcoordinate=a_column)


    def get_row_count(self):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).values('ycoordinate').distinct().count()


    def get_column_count(self):

        Cell = apps.get_model('matrices', 'Cell')

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
        Get Matrix Comments
    """
    def get_matrix_comments(self):

        comment_list = list()

        error_flag = False

        if self.has_blogpost():

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
