#!/usr/bin/python3
###!
# \file         custom.py
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
# The custom template tag
###
import re
import os

from django import template
from django.conf import settings


register = template.Library()
numeric_test = re.compile("^\d+$")


@register.filter
def index(List, i):
	return List[int(i)]

@register.filter
def entry_num_array(List):
	return range(len(List))

@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)

@register.filter
def filename(value):
    return os.path.basename(value.file.name)

@register.simple_tag
def userdateformat(value, argument):
    return value.strftime(argument)
