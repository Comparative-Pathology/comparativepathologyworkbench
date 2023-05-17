#!/usr/bin/python3
###!
# \file         convert_to_ordinal.py
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
# Escape all characters in a string that need escaping
###
from __future__ import unicode_literals

import base64, hashlib

from os import urandom

"""
    Convert a Number to an Ordinal Number 
    eg. '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
        '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th',
        '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th',
        '29th', '30th', '31st'
"""
def convert_to_ordinal(a_number):

    if 11 <= (a_number % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(a_number % 10, 4)]
    
    ordinal_number = str(a_number) + suffix

    return ordinal_number
