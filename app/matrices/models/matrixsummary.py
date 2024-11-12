#!/usr/bin/python3
###!
# \file         matrixsummary.py
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
# The Bench Summary Model - for a VIEW not a table ;-)
###
from __future__ import unicode_literals

from django.db import models


#
#   MATRIX SUMMARY (a VIEW for ALL Benches)
#
class MatrixSummary(models.Model):

    matrix_id = models.IntegerField(default=0, blank=False)
    matrix_title = models.CharField(max_length=255, default='')
    matrix_description = models.TextField(max_length=4095, default='')
    matrix_blogpost = models.CharField(max_length=50, blank=True, default='')
    matrix_created = models.DateTimeField()
    matrix_modified = models.DateTimeField()
    matrix_height = models.IntegerField(default=0, blank=False)
    matrix_width = models.IntegerField(default=0, blank=False)
    matrix_owner = models.CharField(max_length=50, default='')
    matrix_public = models.BooleanField(default=False)
    matrix_locked = models.BooleanField(default=False)
    matrix_authorisation_id = models.IntegerField(default=0, blank=False)
    matrix_authorisation_permitted = models.CharField(max_length=50, default='')
    matrix_authorisation_authority = models.CharField(max_length=12, default='')

    class Meta:
        managed = False
        db_table = 'matrices_bench_summary'

    def __str__(self):

        return f"{self.matrix_id}, \
            {self.matrix_title}, \
            {self.matrix_description}, \
            {self.matrix_blogpost}, \
            {self.matrix_created}, \
            {self.matrix_modified}, \
            {self.matrix_height}, \
            {self.matrix_width}, \
            {self.matrix_owner}, \
            {self.matrix_public}, \
            {self.matrix_locked}, \
            {self.matrix_authorisation_id}, \
            {self.matrix_authorisation_permitted}, \
            {self.matrix_authorisation_authority}"

    def __repr__(self):
        
        return f"{self.matrix_id}, \
            {self.matrix_title}, \
            {self.matrix_description}, \
            {self.matrix_blogpost}, \
            {self.matrix_created}, \
            {self.matrix_modified}, \
            {self.matrix_height}, \
            {self.matrix_width}, \
            {self.matrix_owner}, \
            {self.matrix_public}, \
            {self.matrix_locked}, \
            {self.matrix_authorisation_id}, \
            {self.matrix_authorisation_permitted}, \
            {self.matrix_authorisation_authority}"

    #
    #   If this Bench is Locked, then True, else False
    #
    def is_locked(self):

        if self.matrix_locked is True:
            return True
        else:
            return False

    #
    #   If this Bench is NOT Locked, then True, else False
    #
    def is_not_locked(self):

        if self.matrix_locked is False:
            return True
        else:
            return False

    #
    #   If this Bench is Public, then True, else False
    #
    def is_public(self):

        if self.matrix_public is True:
            return True
        else:
            return False

    #
    #   If this Bench is NOT Public, then True, else False
    #
    def is_not_public(self):

        if self.matrix_public is False:
            return True
        else:
            return False

    #
    #   If this Bench is Unlocked, then True, else False
    #
    def is_unlocked(self):

        if self.matrix_locked is False:
            return True
        else:
            return False

    #
    #   If this Bench is NOT Locked, then True, else False
    #
    def is_not_unlocked(self):

        if self.matrix_locked is True:
            return True
        else:
            return False

    #
    #   If this Bench is Private, then True, else False
    #
    def is_private(self):

        if self.matrix_public is False:
            return True
        else:
            return False

    #
    #   If this Bench is NOT Private, then True, else False
    #
    def is_not_private(self):

        if self.matrix_public is True:
            return True
        else:
            return False

