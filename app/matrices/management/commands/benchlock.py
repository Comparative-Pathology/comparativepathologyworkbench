#!/usr/bin/python3
#
# ##
# \file         benchlock.py
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
# This file contains the Bench Lock admin command USING a Task if possible
# ##
#
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from matrices.models import Matrix

from matrices.routines.get_primary_cpw_environment import get_primary_cpw_environment

from background.tasks import lock_bench_task


#
#   The Bench Lock admin command
#
class Command(BaseCommand):
    help = "Lock Bench USING a Task"

    def add_arguments(self, parser):

        parser.add_argument('bench_lock', type=str, help='Indicates the Id of the Bench to be locked')

        # Named (optional) arguments
        parser.add_argument(
            "--update",
            action="store_true",
            help="No update performed!",
        )

    def handle(self, *args, **options):

        bench_lock = options['bench_lock']

        update = False

        if options["update"]:

            update = True

        out_message = "Update                                                   : {}"\
            .format(update)
        self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Lock Bench                                               : {}"\
            .format(bench_lock)
        self.stdout.write(self.style.SUCCESS(out_message))

        environment = get_primary_cpw_environment()

        out_message = ""
        task_message = ""

        matrix_list = list()

        if bench_lock.lower() == 'all':

            matrix_list = Matrix.objects.all().order_by('id')

        else:

            matrix_list = Matrix.objects.filter(id=bench_lock).order_by('id')

        for matrix in matrix_list:

            if update:

                if environment.is_background_processing():

                    result = lock_bench_task.delay(matrix.id)

                    if result.ready():

                        task_message = result.get(timeout=1)
                        self.stdout.write(self.style.SUCCESS(task_message))

                else:

                    matrix.set_locked()

                    matrix.save()

            out_message = "Program benchlocktask : Bench CPW:{0:06d} lock: {1}!!"\
                .format(matrix.id, matrix.locked)
            self.stdout.write(self.style.SUCCESS(out_message))

        out_message = "Program : Lock Bench TASK Complete!!"
        self.stdout.write(self.style.SUCCESS(out_message))
