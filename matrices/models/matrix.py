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

from requests.exceptions import HTTPError

from matrices.models import Collection

from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment


WORDPRESS_SUCCESS = 'Success!'

class Matrix(models.Model):
    """

    A Bench in the Comparative Pathology Workbench

    Parameters:
        title: The Title of the Bench, Maximum 255 Characters.
        description: The Description of the Bench, Maximum 255 Characters.
        blogpost: The identifier of the associated WordPress BlogPost, in Characters
        created: The Date and Time of Bench Creation.
        modified: The Date and Time of the last Bench Update.
        height: The Height in Pixels of the Cells in this Bench, an Integer.
        width: The Width in Pixels of the Cells in this Bench, an Integer.
        owner: The Owner (User Model) of the Bench
        last_used_collection: The Collecion (Colleciton Model) last used to updte this Bench.

    """

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
        """A Class Method to Create a new Bench."""

        return cls(title=title, description=description, blogpost=blogpost, height=height, width=width, owner=owner)


    def __str__(self):
        """Returns a Partial String Representation of a Bench."""

        str_last_used_collection = ""

        if self.has_last_used_collection():
            str_last_used_collection = str(self.last_used_collection.id)
        else:
            str_last_used_collection = "No Collection"

        return f"CPW:{self.id:06d}, {self.title}"


    def __repr__(self):
        """Returns a Full String Representation of a Bench."""

        str_last_used_collection = ""

        if self.has_last_used_collection():
            str_last_used_collection = str(self.last_used_collection.id)
        else:
            str_last_used_collection = "No Collection"

        return f"{self.id}, {self.title}, {self.description}, {self.blogpost}, {self.created}, {self.modified}, {self.height}, {self.width}, {self.owner.id}, {str_last_used_collection}"


    def is_owned_by(self, a_user):
        """If this Bench is owned by a_user, then True, else False."""

        if self.owner == a_user:
            return True
        else:
            return False


    def set_owner(self, a_user):
        """Set the Owner of the Bench to a_user."""

        self.owner = a_user


    def set_blogpost(self, a_blogpost):
        """Set the Blogpost of the Bench to a_blogpost."""

        self.blogpost = a_blogpost


    def has_no_blogpost(self):
        """If this Bench has NO blogpost, then True, else False."""
        if self.blogpost == '' or self.blogpost == '0':
            return True
        else:
            return False


    def has_blogpost(self):
        """If this Bench has A blogpost, then True, else False."""

        if self.blogpost == '' or self.blogpost == '0':
            return False
        else:
            return True


    def set_last_used_collection(self, a_last_used_collection):
        """Sets the last_used_collection of the Bench to a_last_used_collection."""

        self.last_used_collection = a_last_used_collection


    def set_no_last_used_collection(self):
        """Sets the last_used_collection of the Bench to None."""

        self.last_used_collection = None


    def has_no_last_used_collection(self):
        """If this Bench has NO last_used_collection, then True, else False."""

        if self.last_used_collection is None:
            return True
        else:
            return False

    def has_last_used_collection(self):
        """If this Bench has A last_used_collection, then True, else False."""

        if self.last_used_collection is None:
            return False
        else:
            return True

    def get_matrix(self):
        """Returns the Cells associated with this Bench as a 2 Dimensional Array."""

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

    def get_matrix_cells_with_blog(self):
        """Returns the Cells with Blog Entries associated with this Bench."""

        Cell = apps.get_model('matrices', 'Cell')

        cells = Cell.objects.filter(matrix=self.id)

        matrix_cells = list()

        for cell in cells:

            if cell.has_blogpost():

                matrix_cells.append(cell)

        return matrix_cells


    def validate_matrix(self):
        """Returns the Cells associated with this Bench as a 2 Dimensional Array."""

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
        """Returns ALL the Rows of this Bench."""

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).values('ycoordinate').distinct()


    def get_row(self, a_row):
        """Returns the Row specified by a_row of this Bench."""

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).filter(ycoordinate=a_row)


    def get_columns(self):
        """Returns ALL the Columns of this Bench."""

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).values('xcoordinate').distinct()


    def get_column(self, a_column):
        """Returns the Column specified by a_column of this Bench."""

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).filter(xcoordinate=a_column)


    def get_row_count(self):
        """Returns the total number of Rows of this Bench."""

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).values('ycoordinate').distinct().count()


    def get_column_count(self):
        """Returns the total number of Columns of this Bench."""

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).values('xcoordinate').distinct().count()


    def get_max_row(self):
        """Returns the Maximum Row index of this Bench."""

        row_count = self.get_row_count()

        row_count = row_count - 1

        return row_count


    def get_max_column(self):
        """Returns the Maximum Column index of this Bench."""

        column_count = self.get_column_count()

        column_count = column_count - 1

        return column_count


    def get_matrix_comments(self):
        """Returns the Comments associated with this Bench."""

        comment_list = list()

        error_flag = False

        environment = get_primary_cpw_environment()

        if self.has_blogpost():

            comment_list = environment.get_a_post_comments_from_wordpress(self.blogpost)

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
