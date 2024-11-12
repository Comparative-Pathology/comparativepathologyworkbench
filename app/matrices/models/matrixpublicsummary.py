#!/usr/bin/python3
###!
# \file         matrixpublicsummary.py
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
# The Bench Public Summary Model - for a VIEW not a table ;-)
###
from __future__ import unicode_literals

from django.db import models


#
#   MATRIX PUBLIC SUMMARY (a VIEW for ALL PUBLIC Benches)
#
class MatrixPublicSummary(models.Model):

    matrix_public_id = models.IntegerField(default=0, blank=False)
    matrix_public_title = models.CharField(max_length=255, default='')
    matrix_public_description = models.TextField(max_length=4095, default='')
    matrix_public_blogpost = models.CharField(max_length=50, blank=True, default='')
    matrix_public_created = models.DateTimeField()
    matrix_public_modified = models.DateTimeField()
    matrix_public_height = models.IntegerField(default=0, blank=False)
    matrix_public_width = models.IntegerField(default=0, blank=False)
    matrix_public_owner = models.CharField(max_length=50, default='')
    matrix_public_public = models.BooleanField(default=False)
    matrix_public_locked = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'matrices_bench_public_summary'

    def __str__(self):

        return f"{self.matrix_public_id}, \
            {self.matrix_public_title}, \
            {self.matrix_public_description}, \
            {self.matrix_public_blogpost}, \
            {self.matrix_public_created}, \
            {self.matrix_public_modified}, \
            {self.matrix_public_height}, \
            {self.matrix_public_width}, \
            {self.matrix_public_owner}, \
            {self.matrix_public_public}, \
            {self.matrix_public_locked}"

    def __repr__(self):

        return f"{self.matrix_public_id}, \
            {self.matrix_public_title}, \
            {self.matrix_public_description}, \
            {self.matrix_public_blogpost}, \
            {self.matrix_public_created}, \
            {self.matrix_public_modified}, \
            {self.matrix_public_height}, \
            {self.matrix_public_width}, \
            {self.matrix_public_owner}, \
            {self.matrix_public_public}, \
            {self.matrix_public_locked}"
