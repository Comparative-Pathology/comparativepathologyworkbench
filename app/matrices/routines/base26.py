#!/usr/bin/python3
###!
# \file         base26.py
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
# Convert to and From Base26 (Excel Column Format)
###
from __future__ import unicode_literals

import string
from functools import reduce


#
#   Base26 Class
#
class Base26:

    def divmod_excel(n):

        a, b = divmod(n, 26)

        if b == 0:

            return a - 1, b + 26

        return a, b

    def to_excel(num):

        chars = []

        while num > 0:

            num, d = Base26.divmod_excel(num)

            chars.append(string.ascii_uppercase[d - 1])

        return ''.join(reversed(chars))

    def from_excel(chars):

        return reduce(lambda r, x: r * 26 + x + 1, map(string.ascii_uppercase.index, chars), 0)
