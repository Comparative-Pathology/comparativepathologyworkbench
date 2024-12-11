#!/usr/bin/python3
#
# ##
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
# ##
#
from __future__ import unicode_literals

from django.db import models
from django.apps import apps
from django.contrib.auth.models import User

from matrices.models import Collection

from taggit.models import Tag

from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment


WORDPRESS_SUCCESS = 'Success!'


#
#    The Matrix Manager Class
#
class MatrixManager(models.Manager):

    def get_or_none(self, *args, **kwargs):

        try:

            return self.get(*args, **kwargs)

        except (KeyError, Matrix.DoesNotExist):

            return None


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
        last_used_tag: The Tag (Tag Model) last used to updte this Bench.
        public: Indicates if the Bench is Public (True) or Private (False).
        locked: Indicates if the Bench is Locked (True) or Unlocked (False).

    """

    title = models.CharField(max_length=255, default='')
    description = models.TextField(max_length=4095, default='')
    blogpost = models.CharField(max_length=50, blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    height = models.IntegerField(default=75, blank=False)
    width = models.IntegerField(default=75, blank=False)
    owner = models.ForeignKey(User,
                              related_name='matrices',
                              on_delete=models.DO_NOTHING)
    last_used_collection = models.ForeignKey(Collection,
                                             related_name='collections',
                                             null=True,
                                             on_delete=models.DO_NOTHING)
    last_used_tag = models.ForeignKey(Tag,
                                      related_name='lastused_tags',
                                      null=True,
                                      on_delete=models.DO_NOTHING)
    public = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)

    objects = MatrixManager()

    class Meta:
        verbose_name = 'Bench'
        verbose_name_plural = 'Benches'

    #
    #   A Class Method to Create a new Bench
    #
    @classmethod
    def create(cls, title, description, blogpost, height, width, owner):

        return cls(title=title, description=description, blogpost=blogpost, height=height, width=width, owner=owner)

    #
    #   Returns a Partial String Representation of a Bench
    #
    def __str__(self):

        return f"CPW:{self.id:06d}, {self.title}"

    #
    #   Returns a Full String Representation of a Bench
    #
    def __repr__(self):

        str_last_used_collection = ""

        if self.has_last_used_collection():
            str_last_used_collection = str(self.last_used_collection.id)
        else:
            str_last_used_collection = "No Collection"

        return f"{self.id}, \
            {self.title}, \
            {self.description}, \
            {self.blogpost}, \
            {self.created}, \
            {self.modified}, \
            {self.height}, \
            {self.width}, \
            {self.owner.id}, \
            {self.public}, \
            {self.locked}, \
            {str_last_used_collection}"

    #
    #   If this Bench is owned by a_user, then True, else False
    #
    def is_owned_by(self, a_user):

        if self.owner == a_user:
            return True
        else:
            return False

    #
    #   Set the Owner of the Bench to a_user
    #
    def set_owner(self, a_user):

        self.owner = a_user

    #
    #   Set the Blogpost of the Bench to a_blogpost
    #
    def set_blogpost(self, a_blogpost):

        self.blogpost = a_blogpost

    #
    #   If this Bench has NO blogpost, then True, else False
    #
    def has_no_blogpost(self):

        if self.blogpost == '' or self.blogpost == '0':
            return True
        else:
            return False

    #
    #   If this Bench has A blogpost, then True, else False
    #
    def has_blogpost(self):

        if self.blogpost == '' or self.blogpost == '0':
            return False
        else:
            return True

    #
    #   Sets the last_used_collection of the Bench to a_last_used_collection
    #
    def set_last_used_collection(self, a_last_used_collection):

        self.last_used_collection = a_last_used_collection

    #
    #   Sets the last_used_collection of the Bench to None
    #
    def set_no_last_used_collection(self):

        self.last_used_collection = None

    #
    #   If this Bench has NO last_used_collection, then True, else False
    #
    def has_no_last_used_collection(self):

        if self.last_used_collection is None:
            return True
        else:
            return False

    #
    #   If this Bench has A last_used_collection, then True, else False
    #
    def has_last_used_collection(self):

        if self.last_used_collection is None:
            return False
        else:
            return True

    #
    #   Sets the last_used_tag of the Bench to a_last_used_tag
    #
    def set_last_used_tag(self, a_last_used_tag):

        self.last_used_tag = a_last_used_tag

    #
    #   Sets the last_used_tag of the Bench to None
    #
    def set_no_last_used_tag(self):

        self.last_used_tag = None

    #
    #   If this Bench has NO last_used_tag, then True, else False
    #
    def has_no_last_used_tag(self):

        if self.last_used_tag is None:
            return True
        else:
            return False

    #
    #   If this Bench has A last_used_tag, then True, else False
    #
    def has_last_used_tag(self):

        if self.last_used_tag is None:
            return False
        else:
            return True

    #
    #   If this Bench is Locked, then True, else False
    #
    def is_locked(self):

        if self.locked is True:
            return True
        else:
            return False

    #
    #   If this Bench is NOT Locked, then True, else False
    #
    def is_not_locked(self):

        if self.locked is False:
            return True
        else:
            return False

    #
    #   If this Bench is Public, then True, else False
    #
    def is_public(self):

        if self.public is True:
            return True
        else:
            return False

    #
    #   If this Bench is NOT Public, then True, else False
    #
    def is_not_public(self):

        if self.public is False:
            return True
        else:
            return False

    #
    #   If this Bench is Unlocked, then True, else False
    #
    def is_unlocked(self):

        if self.locked is False:
            return True
        else:
            return False

    #
    #   If this Bench is NOT Locked, then True, else False
    #
    def is_not_unlocked(self):

        if self.locked is True:
            return True
        else:
            return False

    #
    #   If this Bench is Private, then True, else False
    #
    def is_private(self):

        if self.public is False:
            return True
        else:
            return False

    #
    #   If this Bench is NOT Private, then True, else False
    #
    def is_not_private(self):

        if self.public is True:
            return True
        else:
            return False

    #
    #   Sets the Locked field of the Bench to True
    #
    def set_locked(self):

        self.locked = True

    #
    #   Sets the Locked field of the Bench to False
    #
    def set_unlocked(self):

        self.locked = False

    #
    #   Sets the public field of the Bench to True
    #
    def set_public(self):

        self.public = True

    #
    #   Sets the public field of the Bench to False
    #
    def set_private(self):

        self.public = False

    #
    #   Returns the Formatted ID for the Bench
    #
    def get_formatted_id(self):

        return "CPW:" + format(int(self.id), '06d')

    #
    #   Returns the Cells associated with this Bench as a 2 Dimensional Array
    #
    def get_matrix(self):

        Cell = apps.get_model('matrices', 'Cell')

        columns = self.get_columns()
        rows = self.get_rows()

        columnCount = self.get_column_count()
        rowCount = self.get_row_count()

        cells = Cell.objects.filter(matrix=self.id)

        matrix_cells = [[0 for cc in range(columnCount)] for rc in range(rowCount)]

        for i, row in enumerate(rows):

            row_cells = cells.filter(ycoordinate=i)

            for j, column in enumerate(columns):

                matrix_cell = row_cells.filter(xcoordinate=j)[0]

                matrix_cells[i][j] = matrix_cell

        return matrix_cells

    #
    #   Returns the Cells with Images associated with this Bench
    #
    def get_matrix_cells_with_image(self):

        Cell = apps.get_model('matrices', 'Cell')

        cells = Cell.objects.filter(matrix=self.id)

        matrix_cells = list()

        for cell in cells:

            if cell.image is not None:

                if cell.image.id != 0:

                    matrix_cells.append(cell)

        return matrix_cells

    #
    #   Returns the Cells with Blog Entries associated with this Bench
    #
    def get_matrix_cells_with_blog(self):

        Cell = apps.get_model('matrices', 'Cell')

        cells = Cell.objects.filter(matrix=self.id)

        matrix_cells = list()

        for cell in cells:

            if cell.has_blogpost():

                matrix_cells.append(cell)

        return matrix_cells

    #
    #   Returns the Cells associated with this Bench as a 2 Dimensional Array
    #
    def validate_matrix(self):

        Cell = apps.get_model('matrices', 'Cell')

        columns = self.get_columns()
        rows = self.get_rows()

        columnCount = self.get_column_count()
        rowCount = self.get_row_count()

        cells = Cell.objects.filter(matrix=self.id)

        matrix_cells = [[0 for cc in range(columnCount)] for rc in range(rowCount)]

        for i, row in enumerate(rows):

            row_cells = cells.filter(ycoordinate=i)

            for j, column in enumerate(columns):

                matrix_cell = row_cells.filter(xcoordinate=j)[0]

                matrix_cells[i][j] = matrix_cell

        return matrix_cells

    #
    #   Returns ALL the Rows of this Bench
    #
    def get_rows(self):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).values('ycoordinate').distinct()

    #
    #   Returns the Row specified by a_row of this Bench
    #
    def get_row(self, a_row):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).filter(ycoordinate=a_row)

    #
    #   Returns the Row Headers Cells of this Bench
    #
    def get_row_header_cells(self):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).filter(xcoordinate=0).order_by('ycoordinate')

    #
    #   Returns ALL the Columns of this Bench
    #
    def get_columns(self):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).values('xcoordinate').distinct()

    #
    #   Returns the Column specified by a_column of this Bench
    #
    def get_column(self, a_column):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).filter(xcoordinate=a_column)

    #
    #   Returns the Column Header Cells of this Bench
    #
    def get_column_header_cells(self):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).filter(ycoordinate=0).order_by('xcoordinate')

    #
    #   Returns the total number of Rows of this Bench
    #
    def get_row_count(self):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).values('ycoordinate').distinct().count()

    #
    #   Returns the total number of Columns of this Bench
    #
    def get_column_count(self):

        Cell = apps.get_model('matrices', 'Cell')

        return Cell.objects.filter(matrix=self.id).values('xcoordinate').distinct().count()

    #
    #   Returns the Maximum Row index of this Bench
    #
    def get_max_row(self):

        row_count = self.get_row_count()

        row_count = row_count - 1

        return row_count

    #
    #   Returns the Maximum Column index of this Bench
    #
    def get_max_column(self):

        column_count = self.get_column_count()

        column_count = column_count - 1

        return column_count

    #
    #   Returns the Comments associated with this Bench
    #
    def get_matrix_comments(self):

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

        if error_flag is True:

            comment_list = []

        matrixComments = ({
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'blogpost': self.blogpost,
            'comment_list': comment_list
        })

        return matrixComments
