#!/usr/bin/python3
#
# ##
# \file         bench_cell_blog_read.py
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
# This file contains the AJAX bench_read.py view routine
# ##
#
from __future__ import unicode_literals

from django.http import HttpResponse

from matrices.models import Cell


#
#   READ A CELL BLOG
#
def bench_cell_blog_read(request, cell_id):

    htmlString = ''

    object = Cell.objects.get_or_none(id=cell_id)

    if object:

        cell_comments = object.get_cell_comments()

        introString = '<dl class=\"standard\">'\
                      '<dt>Cell Title</dt>'\
                      '<dd>' + object.title[:20] + '</dd>'\
                      '<dt>Description</dt>'\
                      '<dd>' + object.description[:20] + '</dd>'\
                      '</dl>'

        commentsString = ''

        if cell_comments['comment_list']:

            commentsString = '<h3>Commentary</h3>'\
                             '<table>'\
                             '<tr>'\
                             '<th>Date</th>'\
                             '<th>Time</th>'\
                             '<th>Author</th>'\
                             '<th>Comment</th>'\
                             '</tr>'

            for comment in cell_comments['comment_list']:

                commentString = '<tr>'\
                                '<td>' + str(comment['date']) + '</td>'\
                                '<td>' + str(comment['time']) + '</td>'\
                                '<td>' + str(comment['author_name']) + '</td>'\
                                '<td>' + str(comment['content'][:50]) + '</td>'\
                                '</tr>'

                commentsString = commentsString + commentString

            commentsString = commentsString + '</table><p></p>'

        else:

            commentsString = '<p>There are NO Comments for this Cell!</p>'

        htmlString = introString + commentsString

    else:

        htmlString = '<h1>CELL DOES NOT EXIST!!!</h1>'

    return HttpResponse(htmlString)
