#!/usr/bin/python3
#
# ##
# \file         environmentsummary.py
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
# The Environment Summary Model.
# ##
#
from __future__ import unicode_literals

from django.db import models

ENVIRONMENT_NAME_CPW = 'CPW'

ENVIRONMENT_CZI = 'CZI'
ENVIRONMENT_CANADA = 'CANADA'
ENVIRONMENT_COELIAC = 'COELIAC'
ENVIRONMENT_DEVELOPMENT = 'DEVELOPMENT'


#
#    The EnvironmentSummary Manager Class
#
class EnvironmentSummaryManager(models.Manager):

    def get_or_none(self, *args, **kwargs):

        try:

            return self.get(*args, **kwargs)

        except (KeyError, EnvironmentSummary.DoesNotExist):

            return None


#
#   The Environment Summary Model
#
class EnvironmentSummary(models.Model):

    environment_id = models.IntegerField(default=0,
                                         blank=False)
    environment_name = models.CharField(max_length=50,
                                        blank=False,
                                        unique=True)
    environment_location = models.CharField(max_length=25,
                                            blank=False,
                                            unique=True)
    environment_colour = models.CharField(max_length=6,
                                          blank=False)
    environment_wordpress_active = models.BooleanField(default=False)
    environment_background_processing = models.BooleanField(default=False)
    environment_window_refresh_time_milliseconds = models.IntegerField(default=0,
                                                                       blank=False)

    objects = EnvironmentSummaryManager()

    class Meta:
        managed = False
        db_table = 'matrices_environment_summary'

    def __str__(self):
        return f"{self.environment_id}, {self.environment_name}, {self.environment_location}"

    def __repr__(self):
        return f"{self.environment_id}, {self.environment_name}, {self.environment_location}"

    def is_cpw(self):
        if self.environment_name == ENVIRONMENT_NAME_CPW:
            return True
        else:
            return False

    def is_czi(self):
        if self.environment_location == ENVIRONMENT_CZI:
            return True
        else:
            return False

    def is_canada(self):
        if self.environment_location == ENVIRONMENT_CANADA:
            return True
        else:
            return False

    def is_coeliac(self):
        if self.environment_location == ENVIRONMENT_COELIAC:
            return True
        else:
            return False

    def is_development(self):
        if self.environment_location == ENVIRONMENT_DEVELOPMENT:
            return True
        else:
            return False

    def is_wordpress_active(self):
        if self.environment_wordpress_active is True:
            return True
        else:
            return False

    def is_background_processing(self):
        if self.environment_background_processing is True:
            return True
        else:
            return False
