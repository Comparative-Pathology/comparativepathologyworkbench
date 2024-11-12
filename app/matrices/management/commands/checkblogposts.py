#!/usr/bin/python3
# \file         checkblogposts.py
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
# This file contains the Check Blogposts admin command
#
###
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from matrices.models import Matrix

from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment
from matrices.routines import get_credential_for_user

WORDPRESS_SUCCESS = 'Success!'


#
# The Check Blogposts admin command
#
class Command(BaseCommand):
    help = "Check Blogposts"

    def add_arguments(self, parser):

        parser.add_argument('check_bench', type=str, help='Indicates the Id of the Bench to be checked')

        # Named (optional) arguments
        parser.add_argument(
            "--update",
            action="store_true",
            help="No update performed!",
        )

    def handle(self, *args, **options):

        check_bench = options['check_bench']

        update = False

        if options["update"]:

            update = True

        out_message = "Update                                                   : {}"\
            .format(update)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Check Bench                                              : {}"\
            .format(check_bench)
        self.stdout.write(self.style.SUCCESS(out_message))

        environment = get_primary_cpw_environment()

        benchCount = 0
        benchBlogCount = 0
        benchNoBlogCount = 0
        benchBlogNoExistsCount = 0
        cellCount = 0
        cellBlogCount = 0
        cellNoBlogCount = 0
        cellBlogNoExistsCount = 0

        out_message = ""

        matrix_list = list()

        if check_bench.lower() == 'all':

            matrix_list = Matrix.objects.all().order_by('id')

        else:

            matrix_list = Matrix.objects.filter(id=check_bench).order_by('id')

        for matrix in matrix_list:

            credential = get_credential_for_user(matrix.owner)

            benchCount = benchCount + 1

            if matrix.has_blogpost():

                if credential.has_apppwd() and environment.is_wordpress_active():

                    blogpost = environment.get_a_post_from_wordpress(matrix.blogpost)

                    if blogpost['status'] == WORDPRESS_SUCCESS:

                        benchBlogCount = benchBlogCount + 1

                    else:

                        benchBlogNoExistsCount = benchBlogNoExistsCount + 1

                        out_message = "Bench CPW:{0:06d} has Blogpost that does NOT EXIST!!"\
                            .format(matrix.id)
                        self.stdout.write(self.style.SUCCESS(out_message))

                        if update:

                            returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                                     matrix.title,
                                                                                     matrix.description)

                            if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                post_id = returned_blogpost['id']

                                matrix.set_blogpost(post_id)
                                matrix.save()

                                out_message = "Bench CPW:{0:06d} has NEW Blogpost: {1}!!"\
                                    .format(matrix.id, post_id)
                                self.stdout.write(self.style.SUCCESS(out_message))

            else:

                benchNoBlogCount = benchNoBlogCount + 1

                out_message = "Bench CPW:{0:06d} has NO Blogpost!!"\
                    .format(matrix.id)
                self.stdout.write(self.style.SUCCESS(out_message))

                if update:

                    if credential.has_apppwd() and environment.is_wordpress_active():

                        returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                                 matrix.title,
                                                                                 matrix.description)

                        if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                            post_id = returned_blogpost['id']

                            matrix.set_blogpost(post_id)
                            matrix.save()

                            out_message = "Bench CPW:{0:06d} has NEW Blogpost: {1}!!"\
                                .format(matrix.id, post_id)
                            self.stdout.write(self.style.SUCCESS(out_message))

            matrix_cells = list()

            matrix_cells = matrix.get_matrix_cells_with_image()

            for cell in matrix_cells:

                cellCount = cellCount + 1

                if cell.has_blogpost():

                    if credential.has_apppwd() and environment.is_wordpress_active():

                        blogpost = environment.get_a_post_from_wordpress(cell.blogpost)

                        if blogpost['status'] == WORDPRESS_SUCCESS:

                            cellBlogCount = cellBlogCount + 1

                        else:

                            cellBlogNoExistsCount = cellBlogNoExistsCount + 1

                            out_message = "Image Name : {0}"\
                                .format(cell.image.name)
                            self.stdout.write(self.style.SUCCESS(out_message))

                            out_message = "Cell  CPW:{0:06d}_{1:012d} has Blogpost that does NOT EXIST!!"\
                                .format(matrix.id, cell.id)
                            self.stdout.write(self.style.SUCCESS(out_message))

                            if update:

                                returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                                         cell.title,
                                                                                         cell.description)

                                if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                    post_id = returned_blogpost['id']

                                    cell.set_blogpost(post_id)
                                    cell.save()

                                    out_message = "Cell  CPW:{0:06d}_{1:012d} has NEW Blogpost: {2}!!"\
                                        .format(matrix.id, cell.id, post_id)
                                    self.stdout.write(self.style.SUCCESS(out_message))

                else:

                    cellNoBlogCount = cellNoBlogCount + 1

                    out_message = "Image Name : {0}"\
                        .format(cell.image.name)
                    self.stdout.write(self.style.SUCCESS(out_message))

                    out_message = "Cell  CPW:{0:06d}_{1:012d} has NO Blogpost!!"\
                        .format(matrix.id, cell.id)
                    self.stdout.write(self.style.SUCCESS(out_message))

                    if update:

                        if credential.has_apppwd() and environment.is_wordpress_active():

                            returned_blogpost = environment.post_a_post_to_wordpress(credential,
                                                                                     cell.title,
                                                                                     cell.description)

                            if returned_blogpost['status'] == WORDPRESS_SUCCESS:

                                post_id = returned_blogpost['id']

                                cell.set_blogpost(post_id)
                                cell.save()

                                out_message = "Cell  CPW:{0:06d}_{1:012d} has NEW Blogpost              : {2}!!"\
                                    .format(matrix.id, cell.id, post_id)
                                self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Benches                                  : {}"\
            .format(benchCount)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Benches WITH a Blogpost                  : {}"\
            .format(benchBlogCount)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Benches WITH NO Blogpost                 : {}"\
            .format(benchNoBlogCount)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Benches WITH a NON-EXISTING Blogpost     : {}"\
            .format(benchBlogNoExistsCount)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Cells with an Image                      : {}"\
            .format(cellCount)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Cells with an Image and a Blogpost       : {}"\
            .format(cellBlogCount)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Cells with an Image WITHOUT a Blogpost   : {}"\
            .format(cellNoBlogCount)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Total Number of Cells WITH a NON-EXISTING Blogpost       : {}"\
            .format(cellBlogNoExistsCount)
        self.stdout.write(self.style.SUCCESS(out_message))
