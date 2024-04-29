#!/usr/bin/python3
###!
# \file         aggregate_bench_cell_blog_read.py
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
#
# This file contains the AJAX aggregate_bench_cell_blog_read.py view routine
#
###
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from frontend_forms.utils import get_object_by_uuid_or_404

from matrices.models import Cell

from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment

#
# READ A BENCH
#
@login_required()
def aggregate_bench_cell_blog_read(request, cell_id):

    environment = get_primary_cpw_environment()

    object = get_object_by_uuid_or_404(Cell, cell_id)

    cell_blogpost = environment.get_a_post_from_wordpress(object.blogpost)

    cell_comments = object.get_cell_comments()

    htmlString = ''
    imageString = ''

    introString = '<table border="0">'\
        '<tr>'\
            '<th style="text-align: left; width: 100px;">Date</th>'\
            '<th style="text-align: left; width: 100px;">Time</th>'\
            '<th style="text-align: left; width: 100px;">Author</th>'\
            '<th style="text-align: left;">Post</th>'\
        '</tr>'\
        '<tr>'\
            '<td style="text-align: left; vertical-align: text-top;">' + cell_blogpost['date'] + '</td>'\
            '<td style="text-align: left; vertical-align: text-top;">' + cell_blogpost['time'] + '</td>'\
            '<td style="text-align: left; vertical-align: text-top;">' + cell_blogpost['author'] + '</td>'\
            '<td style="text-align: left; vertical-align: text-top;">' + cell_blogpost['content'] + '</td>'\
        '</tr>'\
        '<tr>'\
            '<td>&nbsp;</td>'\
            '<td>&nbsp;</td>'\
            '<td>&nbsp;</td>'\
            '<td>&nbsp;</td>'\
        '</tr>'

    if object.image.viewer_url != '':

        imageString = '<tr>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
            '</tr>'\
            '<tr>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>'\
                    '<a href=\"' + object.image.viewer_url + '\" target="_blank"><img alt=\"' + object.image.name + '\" title=\"' + object.image.name + '\" style=\"width:450px; height:450px;\" src=\"' + object.image.birdseye_url + '\" ></a>'\
                '</td>'\
            '</tr>'\
            '<tr>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
            '</tr>'
    
    introString = introString + imageString

    commentsString = ''

    if cell_comments['comment_list']:

        commentsString = '<tr>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
            '</tr>'\
            '<tr>'\
                '<th style="text-align: left; width: 100px;">Date</th>'\
                '<th style="text-align: left; width: 100px;">Time</th>'\
                '<th style="text-align: left; width: 100px;">Author</th>'\
                '<th style="text-align: left;">Comment</th>'\
            '</tr>'

        for comment in cell_comments['comment_list']:

            commentString = '<tr>'\
                    '<td style="text-align: left; vertical-align: text-top;">' + str(comment['date']) + '</td>'\
                    '<td style="text-align: left; vertical-align: text-top;">' + str(comment['time']) + '</td>'\
                    '<td style="text-align: left; vertical-align: text-top;">' + str(comment['author_name']) + '</td>'\
                    '<td style="text-align: left; vertical-align: text-top;">' + str(comment['content']) + '</td>'\
                '</tr>'\
                '<tr>'\
                    '<td>&nbsp;</td>'\
                    '<td>&nbsp;</td>'\
                    '<td>&nbsp;</td>'\
                    '<td>&nbsp;</td>'\
                '</tr>'
            
            commentsString = commentsString + commentString
        
        commentsString = commentsString + '</table>'

    else:

        commentsString = '<tr>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
            '</tr>'\
            '<tr>'\
                '<th style="text-align: left; width: 100px;">Date</th>'\
                '<th style="text-align: left; width: 100px;">Time</th>'\
                '<th style="text-align: left; width: 100px;">Author</th>'\
                '<th style="text-align: left;">Comment</th>'\
            '</tr>'\
            '<tr>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>&nbsp;</td>'\
                '<td>No Cell Comments!</td>'\
            '</tr></table>'    

    htmlString = introString + commentsString


    return HttpResponse(htmlString)
