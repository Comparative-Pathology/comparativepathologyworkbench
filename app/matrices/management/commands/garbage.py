#!/usr/bin/python3
#
# ##
# \file         garbage.py
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
# This file contains the garbage admin command
# ##
#
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from faker import Faker

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Collection
from matrices.models import Image

ALL = "all"
MATRIX = "matrix"
COLLECTION = "collection"
IMAGE = "image"
CELL = "cell"
TABLES = {"matrix", "cell", "collection", "image"}
MATRIX_COLUMNS = {"title", "description", 'all'}
CELL_COLUMNS = {"title", "description", 'all'}
COLLECTION_COLUMNS = {"title", "description", 'all'}
IMAGE_COLUMNS = {"name", "comment", 'all'}
TITLE = "title"
DESCRIPTION = "description"
NAME = "name"
COMMENT = "comment"


#
# The Mailer Admin Command
#
class Command(BaseCommand):
    help = "Creates Garbage Data"

    def add_arguments(self, parser):

        parser.add_argument('table', type=str, help='Indicates the Table to be updated')
        parser.add_argument('column', type=str, help='Indicates the Column to be updated')
        parser.add_argument('identifier', type=str, help='Indicates the Row to be updated')
        parser.add_argument('output', type=str, help='Indicates the Recovery File to be Generated')

        # Named (optional) arguments
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear the Fields!",
        )

        parser.add_argument(
            "--update",
            action="store_true",
            help="No update performed!",
        )

    def handle(self, *args, **options):

        table = options['table'].lower()
        column = options['column'].lower()
        identifier = options['identifier'].lower()
        output = options['output']

        proceed = True
        update = False
        update_matrix = False
        update_cell = False
        update_collection = False
        update_image = False

        if options["update"]:

            update = True

        clear = False

        if options["clear"]:

            clear = True

        out_message = "Update                                         : {}"\
            .format(update)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Clear                                          : {}"\
            .format(clear)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Table                                          : {}"\
            .format(table)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Column                                         : {}"\
            .format(column)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Identifier                                     : {}"\
            .format(identifier)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Output                                         : {}"\
            .format(output)
        self.stdout.write(self.style.SUCCESS(out_message))

        if table not in TABLES:
            out_message = "Supplied Table not Matrix/Cell/Image           : {}"\
                .format(table)
            self.stdout.write(self.style.ERROR(out_message))

        if table == MATRIX:
            update_matrix = True
            if column not in MATRIX_COLUMNS:
                out_message = "Supplied Column not Title/Description/All      : {}"\
                    .format(column)
                self.stdout.write(self.style.ERROR(out_message))
                proceed = False

        if table == CELL:
            update_cell = True
            if column not in CELL_COLUMNS:
                out_message = "Supplied Column not Title/Description/All      : {}"\
                    .format(column)
                self.stdout.write(self.style.ERROR(out_message))
                proceed = False

        if table == COLLECTION:
            update_collection = True
            if column not in COLLECTION_COLUMNS:
                out_message = "Supplied Column not Title/Description/All      : {}"\
                    .format(column)
                self.stdout.write(self.style.ERROR(out_message))
                proceed = False

        if table == IMAGE:
            update_image = True
            if column not in IMAGE_COLUMNS:
                out_message = "Supplied Column not Name/Comment/All           : {}"\
                    .format(column)
                self.stdout.write(self.style.ERROR(out_message))
                proceed = False

        if identifier.isnumeric():
            if int(identifier) < 1:
                out_message = "Supplied Identifer must be GT 0                : {}"\
                    .format(identifier)
                self.stdout.write(self.style.ERROR(out_message))
                proceed = False
        else:
            if identifier != ALL:
                out_message = "Supplied Identifer is not ALL or a Number      : {}"\
                    .format(identifier)
                self.stdout.write(self.style.ERROR(out_message))
                proceed = False

        if proceed:

            output_file = open(output, "w")

            if update_matrix:

                if identifier == ALL:

                    matrices = Matrix.objects.all().order_by('id')

                    for matrix in matrices:

                        old_title = matrix.title.replace("'", "''")
                        old_description = matrix.description.replace("'", "''")

                        if clear:

                            if column == ALL:

                                matrix.title = ''
                                matrix.description = ''

                            else:

                                if column == TITLE:

                                    matrix.title = ''

                                if column == DESCRIPTION:

                                    matrix.description = ''

                        else:

                            fake = Faker()

                            if column == ALL:

                                matrix.title = fake.text()
                                matrix.description = fake.text()

                            else:

                                if column == TITLE:

                                    matrix.title = fake.text()

                                if column == DESCRIPTION:

                                    matrix.description = fake.text()

                        if update:

                            matrix.save()

                            out_message = "Matrix SAVED!                                  : {}"\
                                .format(matrix.id)
                            self.stdout.write(self.style.SUCCESS(out_message))

                        else:

                            out_message = "Matrix NOT SAVED!                              : {}"\
                                .format(matrix.id)
                            self.stdout.write(self.style.ERROR(out_message))

                        output_file.write("UPDATE public.matrices_matrix SET title = \'" + old_title +
                                              "\', description = \'" + old_description + "\' WHERE id = " +
                                              str(matrix.id) + ";\n")

                else:

                    if Matrix.objects.filter(pk=identifier).exists():

                        matrix = Matrix.objects.get(pk=identifier)

                        old_title = matrix.title.replace("'", "''")
                        old_description = matrix.description.replace("'", "''")

                        if clear:

                            if column == ALL:

                                matrix.title = ''
                                matrix.description = ''

                            else:

                                if column == TITLE:

                                    matrix.title = ''

                                if column == DESCRIPTION:

                                    matrix.description = ''

                        else:

                            fake = Faker()

                            if column == ALL:

                                matrix.title = fake.text()
                                matrix.description = fake.text()

                            else:

                                if column == TITLE:

                                    matrix.title = fake.text()

                                if column == DESCRIPTION:

                                    matrix.description = fake.text()

                        if update:

                            matrix.save()

                            out_message = "Matrix SAVED!                                  : {}"\
                                .format(identifier)
                            self.stdout.write(self.style.SUCCESS(out_message))

                        else:

                            out_message = "Matrix NOT SAVED!                              : {}"\
                                .format(identifier)
                            self.stdout.write(self.style.ERROR(out_message))

                        output_file.write("UPDATE public.matrices_matrix SET title = \'" + old_title +
                                          "\', description = \'" + old_description + "\' WHERE id = " + str(identifier) +
                                          ";")

                    else:

                        out_message = "There is NO Matrix for the Supplied Identifer! : {}"\
                            .format(identifier)
                        self.stdout.write(self.style.ERROR(out_message))

            if update_collection:

                if identifier == ALL:

                    collections = Collection.objects.all().order_by('id')

                    for collection in collections:

                        old_title = collection.title.replace("'", "''")
                        old_description = collection.description.replace("'", "''")

                        if clear:

                            if column == ALL:

                                collection.title = ''
                                collection.description = ''

                            else:

                                if column == TITLE:

                                    collection.title = ''

                                if column == DESCRIPTION:

                                    collection.description = ''

                        else:

                            fake = Faker()

                            if column == ALL:

                                collection.title = fake.text()
                                collection.description = fake.text()

                            else:

                                if column == TITLE:

                                    collection.title = fake.text()

                                if column == DESCRIPTION:

                                    collection.description = fake.text()

                        if update:

                            collection.save()

                            out_message = "Collection SAVED!                             : {}"\
                                .format(collection.id)
                            self.stdout.write(self.style.SUCCESS(out_message))

                        else:

                            out_message = "Collection NOT SAVED!                         : {}"\
                                .format(collection.id)
                            self.stdout.write(self.style.ERROR(out_message))

                        output_file.write("UPDATE public.matrices_collection SET title = \'" + old_title +
                                              "\', description = \'" + old_description + "\' WHERE id = " +
                                              str(collection.id) + ";\n")

                else:

                    if Collection.objects.filter(pk=identifier).exists():

                        collection = Collection.objects.get(pk=identifier)

                        old_title = collection.title.replace("'", "''")
                        old_description = collection.description.replace("'", "''")

                        if clear:

                            if column == ALL:

                                collection.title = ''
                                collection.description = ''

                            else:

                                if column == TITLE:

                                    collection.title = ''

                                if column == DESCRIPTION:

                                    collection.description = ''

                        else:

                            fake = Faker()

                            if column == ALL:

                                collection.title = fake.text()
                                collection.description = fake.text()

                            else:

                                if column == TITLE:

                                    collection.title = fake.text()

                                if column == DESCRIPTION:

                                    collection.description = fake.text()

                        if update:

                            collection.save()

                            out_message = "Collection SAVED!                             : {}"\
                                .format(identifier)
                            self.stdout.write(self.style.SUCCESS(out_message))

                        else:

                            out_message = "Collection NOT SAVED!                         : {}"\
                                .format(identifier)
                            self.stdout.write(self.style.ERROR(out_message))

                        output_file.write("UPDATE public.matrices_collection SET title = \'" + old_title +
                                          "\', description = \'" + old_description + "\' WHERE id = " +
                                          str(identifier) +
                                          ";")

                    else:

                        out_message = "There is NO Collection for the Supplied Identifer! : {}"\
                            .format(identifier)
                        self.stdout.write(self.style.ERROR(out_message))

            if update_cell:

                if identifier == ALL:

                    cells = Cell.objects.all().order_by('id')

                    for cell in cells:

                        old_title = cell.title.replace("'", "''")
                        old_description = cell.description.replace("'", "''")

                        if clear:

                            if column == ALL:

                                cell.title = ''
                                cell.description = ''

                            else:

                                if column == TITLE:

                                    cell.title = ''

                                if column == DESCRIPTION:

                                    cell.description = ''

                        else:

                            fake = Faker()

                            if column == ALL:

                                cell.title = fake.text()
                                cell.description = fake.text()

                            else:

                                if column == TITLE:

                                    cell.title = fake.text()

                                if column == DESCRIPTION:

                                    cell.description = fake.text()

                        if update:

                            cell.save()

                            out_message = "Cell SAVED!                                    : {}"\
                                .format(cell.id)
                            self.stdout.write(self.style.SUCCESS(out_message))

                        else:

                            out_message = "Cell NOT SAVED!                                : {}"\
                                .format(cell.id)
                            self.stdout.write(self.style.ERROR(out_message))

                        output_file.write("UPDATE public.matrices_cell SET title = \'" + old_title +
                                          "\', description = \'" + old_description + "\' WHERE id = " +
                                          str(cell.id) + ";\n")

                else:

                    if Cell.objects.filter(pk=identifier).exists():

                        cell = Cell.objects.get(pk=identifier)

                        old_title = cell.title.replace("'", "''")
                        old_description = cell.description.replace("'", "''")

                        if clear:

                            if column == ALL:

                                cell.title = ''
                                cell.description = ''

                            else:

                                if column == TITLE:

                                    cell.title = ''

                                if column == DESCRIPTION:

                                    cell.description = ''

                        else:

                            fake = Faker()

                            if column == ALL:

                                cell.title = fake.text()
                                cell.description = fake.text()

                            else:

                                if column == TITLE:

                                    cell.title = fake.text()

                                if column == DESCRIPTION:

                                    cell.description = fake.text()

                        if update:

                            cell.save()

                            out_message = "Cell SAVED!                                    : {}"\
                                .format(cell.id)
                            self.stdout.write(self.style.SUCCESS(out_message))

                        else:

                            out_message = "Cell NOT SAVED!                                : {}"\
                                .format(cell.id)
                            self.stdout.write(self.style.ERROR(out_message))

                        output_file.write("UPDATE public.matrices_cell SET title = \'" + old_title +
                                          "\', description = \'" + old_description + "\' WHERE id = " +
                                          str(identifier) +
                                          ";")

                    else:

                        out_message = "There is NO Cell for the Supplied Identifer!   : {}"\
                            .format(identifier)
                        self.stdout.write(self.style.ERROR(out_message))

            if update_image:

                if identifier == ALL:

                    images = Image.objects.all().order_by('id')

                    for image in images:

                        old_name = image.name.replace("'", "''")
                        old_comment = image.comment.replace("'", "''")

                        if clear:

                            if column == ALL:

                                image.name = ''
                                image.comment = ''

                            else:

                                if column == NAME:

                                    image.name = ''

                                if column == COMMENT:

                                    image.comment = ''

                        else:

                            fake = Faker()

                            if column == ALL:

                                image.name = fake.text()
                                image.comment = fake.text()

                            else:

                                if column == NAME:

                                    image.name = fake.text()

                                if column == COMMENT:

                                    image.comment = fake.text()

                        if update:

                            image.save()

                            out_message = "Image SAVED!                                   : {}"\
                                .format(image.id)
                            self.stdout.write(self.style.SUCCESS(out_message))

                        else:

                            out_message = "Image NOT SAVED!                               : {}"\
                                .format(image.id)
                            self.stdout.write(self.style.ERROR(out_message))

                        output_file.write("UPDATE public.matrices_image SET name = \'" + old_name +
                                          "\', comment = \'" + old_comment + "\' WHERE id = " +
                                          str(image.id) + ";\n")

                else:

                    if Image.objects.filter(pk=identifier).exists():

                        image = Image.objects.get(pk=identifier)

                        old_name = image.name.replace("'", "''")
                        old_comment = image.comment.replace("'", "''")

                        if clear:

                            if column == ALL:

                                image.name = ''
                                image.comment = ''

                            else:

                                if column == NAME:

                                    image.name = ''

                                if column == COMMENT:

                                    image.comment = ''

                        else:

                            fake = Faker()

                            if column == ALL:

                                image.name = fake.text()
                                image.comment = fake.text()

                            else:

                                if column == NAME:

                                    image.name = fake.text()

                                if column == COMMENT:

                                    image.comment = fake.text()

                        if update:

                            image.save()

                            out_message = "Image SAVED!                                   : {}"\
                                .format(image.id)
                            self.stdout.write(self.style.SUCCESS(out_message))

                        else:

                            out_message = "Image NOT SAVED!                               : {}"\
                                .format(image.id)
                            self.stdout.write(self.style.ERROR(out_message))

                        output_file.write("UPDATE public.matrices_image SET name = \'" + old_name +
                                          "\', comment = \'" + old_comment + "\' WHERE id = " + str(identifier) +
                                          ";")

                    else:

                        out_message = "There is NO Image for the Supplied Identifer!  : {}"\
                            .format(identifier)
                        self.stdout.write(self.style.ERROR(out_message))

            output_file.close()
