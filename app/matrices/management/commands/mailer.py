#!/usr/bin/python3
#
# ##
# \file         mailer.py
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
# This file contains the mailer admin command
# ##
#
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
import magic
import os

from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings

from matrices.routines import get_primary_cpw_environment


#
# The Mailer Admin Command
#
class Command(BaseCommand):
    help = "Mails out a Test Email"

    def add_arguments(self, parser):

        parser.add_argument('-a', '--attachment', type=str, help='Supply an Attachment', )
        parser.add_argument('-s', '--subject', type=str, help='Supply a Subject', )
        parser.add_argument('-m', '--message', type=str, help='Supply a Message', )
        parser.add_argument('-r', '--recipient', type=str, help='Supply a Recipient', )

    def handle(self, *args, **options):

        attachment = False
        subject = False
        message = False
        recipient = False

        subject_text = ''
        message_text = ''
        recipient_text = ''

        recipient_list = list()

        if options["attachment"]:

            attachment = True

        if options["subject"]:

            subject = True

        if options["message"]:

            message = True

        if options["recipient"]:

            recipient = True

        if attachment:

            attachment_file = options["attachment"]

            attachment_path = '{attachment}'.format(attachment=attachment_file)

            file_path = settings.BASE_DIR / attachment_path

            with open(file_path, 'rb') as file:

                file_content = file.read()

            mime_type = magic.from_buffer(file_content, mime=True)

            file_name = os.path.basename(attachment_path)

        environment = get_primary_cpw_environment()

        now = timezone.now()

        if subject:

            subject_text = options["subject"]

        else:

            subject_text = 'A Time Check'

        if message:

            message_text = options["message"]

        else:

            message_text = 'Here is the time : ' + str(now)

        if recipient:

            recipient_text = options["recipient"]
            recipient_list.append(recipient_text)

        else:

            recipient_list.append('edgutcellatlas-cpw@mlist.is.ed.ac.uk')

        email_from = environment.from_email

        email = EmailMessage(subject_text, message_text, email_from, recipient_list)

        if attachment:

            email.attach(file_name, file_content, mime_type)

        email.send()
