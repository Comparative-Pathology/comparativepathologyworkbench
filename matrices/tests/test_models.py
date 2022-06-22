#!/usr/bin/python3
###!
# \file         test_models.py
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
# This test tests the Matrix, Profile, Type, Protocol, Server, Command, Image, Cell, Blog and Credential models
###
from __future__ import unicode_literals

from django.test import TestCase

from django.utils import timezone

from django.contrib.auth.models import User

from matrices.models import Matrix
from matrices.models import Cell
from matrices.models import Type
from matrices.models import Protocol
from matrices.models import Server
from matrices.models import Command
from matrices.models import Image
from matrices.models import Blog
from matrices.models import Credential

from matrices.models import Profile


class MatrixTest(TestCase):

    def setUp(self):

        self.matrix_owner = User.objects.create(username="fbloggs69", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.matrix_not_owner = User.objects.create(username="fbloggs96", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())

        self.owner = User.objects.create(username="fbloggs70", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())

        self.credential = Credential.objects.create(username="fbloggs69", wordpress=0, apppwd="credential_apppwd", owner=self.owner)

        self.matrix_A = Matrix.objects.create(id=99, title="matrix_title", description="matrix_description", blogpost="matrix_blogpost", created=timezone.now(), modified=timezone.now(), height=100, width=100, owner=self.owner )

        self.cell_1_A = Cell.objects.create(matrix=self.matrix_A, title="cell_1", description="cell_description", xcoordinate=0, ycoordinate=0, blogpost="cell_blogpost", image=None)
        self.cell_2_A = Cell.objects.create(matrix=self.matrix_A, title="cell_2", description="cell_description", xcoordinate=1, ycoordinate=0, blogpost="cell_blogpost", image=None)

        self.matrix_B = Matrix.objects.create(id=98, title="matrix_title", description="matrix_description", blogpost="matrix_blogpost", created=timezone.now(), modified=timezone.now(), height=100, width=100, owner=self.owner )

        self.cell_1_B = Cell.objects.create(matrix=self.matrix_B, title="cell_1", description="cell_description", xcoordinate=0, ycoordinate=0, blogpost="cell_blogpost", image=None)
        self.cell_2_B = Cell.objects.create(matrix=self.matrix_B, title="cell_2", description="cell_description", xcoordinate=0, ycoordinate=1, blogpost="cell_blogpost", image=None)

        self.matrix_C= Matrix.objects.create(id=97, title="matrix_title", description="matrix_description", blogpost="", created=timezone.now(), modified=timezone.now(), height=100, width=100, owner=self.owner )

        self.image_type = Type.objects.create(name="type_name", owner=self.owner)
        self.image_server = Server.objects.create(name="server_name", url="server_url", uid="server_uid", pwd="server_pwd", type=self.image_type, owner=self.owner)

        self.image = Image.objects.create(identifier=0, name="image_name", server=self.image_server, viewer_url="image_viewer_url", birdseye_url="image_birdseye_url", owner=self.owner, active=True, roi=1)

        self.cell_1_1_C = Cell.objects.create(matrix=self.matrix_C, title="cell_1_1", description="Row_1_Column_1", xcoordinate=0, ycoordinate=0, blogpost="1", image=self.image)
        self.cell_1_2_C = Cell.objects.create(matrix=self.matrix_C, title="cell_1_2", description="Row_1_Column_2", xcoordinate=0, ycoordinate=1, blogpost="1", image=self.image)
        self.cell_2_1_C = Cell.objects.create(matrix=self.matrix_C, title="cell_2_1", description="Row_2_Column_1", xcoordinate=1, ycoordinate=0, blogpost="1", image=self.image)
        self.cell_2_2_C = Cell.objects.create(matrix=self.matrix_C, title="cell_2_2", description="Row_2_Column_2", xcoordinate=1, ycoordinate=1, blogpost="1", image=self.image)

        self.admin = Credential.objects.create(username="admin", wordpress=1, apppwd="credential_apppwd", owner=self.owner)

        self.protocol = Protocol.objects.create(name="https", owner=self.owner)

        self.get_blog = Blog.objects.create(name="GetAPost", application="wp-json/wp/v2", preamble="posts", postamble="", protocol=self.protocol, url="workbench-czi-cpw.mvm.ed.ac.uk/wordpress", owner=self.owner)
        self.post_blog = Blog.objects.create(name="PostAPost", application="wp-json/wp/v2", preamble="posts", postamble="", protocol=self.protocol, url="workbench-czi-cpw.mvm.ed.ac.uk/wordpress", owner=self.owner)
        self.blog_comments = Blog.objects.create(name="GetPostComments", application="wp-json/wp/v2", preamble="comments?post=", postamble="", protocol=self.protocol, url="workbench-czi-cpw.mvm.ed.ac.uk/wordpress", owner=self.owner)
        self.blog_comment_post = Blog.objects.create(name="PostAComment", application="wp-json/wp/v2", preamble="comments", postamble="", protocol=self.protocol, url="workbench-czi-cpw.mvm.ed.ac.uk/wordpress", owner=self.owner)
        self.blog_delete = Blog.objects.create(name="DeletePost", application="wp-json/wp/v2", preamble="posts", postamble="", protocol=self.protocol, url="workbench-czi-cpw.mvm.ed.ac.uk/wordpress", owner=self.owner)

    def test_matrix_creation(self):

        ordinary_matrix = Matrix(id=1, title="ordinary_matrix", description="matrix_description", blogpost="matrix_blogpost", created=timezone.now(), modified=timezone.now(), height=100, width=100, owner=self.matrix_owner )
        ordinary_matrix_no_blogpost = Matrix(id=1, title="ordinary_matrix", description="matrix_description", blogpost="", created=timezone.now(), modified=timezone.now(), height=100, width=100, owner=self.matrix_owner )
        ordinary_matrix_too_small = Matrix(id=1, title="ordinary_matrix_too_small", description="matrix_description", blogpost="matrix_blogpost", created=timezone.now(), modified=timezone.now(), height=70, width=70, owner=self.matrix_owner )
        ordinary_matrix_too_big = Matrix(id=1, title="ordinary_matrix_too_big", description="matrix_description", blogpost="matrix_blogpost", created=timezone.now(), modified=timezone.now(), height=460, width=460, owner=self.matrix_owner )

        self.assertTrue(isinstance(ordinary_matrix, Matrix))

        self.assertEqual(ordinary_matrix.__str__(), str(ordinary_matrix.id) + ", " + ordinary_matrix.title + ", " + ordinary_matrix.description + ", " + ordinary_matrix.blogpost + ", " + str(ordinary_matrix.owner.id))
        self.assertEqual(ordinary_matrix.__unicode__(), str(ordinary_matrix.id) + ", " + ordinary_matrix.title + ", " + ordinary_matrix.description + ", " + ordinary_matrix.blogpost + ", " + str(ordinary_matrix.created) + ", " + str(ordinary_matrix.modified) + ", " + str(ordinary_matrix.height) + ", " + str(ordinary_matrix.width) + ", " + str(ordinary_matrix.owner.id))

        self.assertEqual(ordinary_matrix.has_no_blogpost(),False)
        self.assertEqual(ordinary_matrix_no_blogpost.has_no_blogpost(),True)

        self.assertEqual(ordinary_matrix.has_blogpost(),True)
        self.assertEqual(ordinary_matrix_no_blogpost.has_blogpost(),False)

        self.assertEqual(ordinary_matrix.is_owned_by(self.matrix_owner),True)
        self.assertEqual(ordinary_matrix.is_owned_by(self.matrix_not_owner),False)

        ordinary_matrix.set_owner(self.matrix_not_owner)

        self.assertEqual(ordinary_matrix.is_owned_by(self.matrix_owner),False)
        self.assertEqual(ordinary_matrix.is_owned_by(self.matrix_not_owner),True)

        ordinary_matrix.set_blogpost("")

        self.assertEqual(ordinary_matrix.has_no_blogpost(),True)

        ordinary_matrix.set_blogpost("87654321")

        self.assertEqual(ordinary_matrix.blogpost, "87654321")

        self.assertEqual(ordinary_matrix.has_no_blogpost(),False)


        x_coordinate_1 = {'xcoordinate': 0}
        x_coordinate_2 = {'xcoordinate': 1}

        self.assertEqual(self.matrix_A.get_column_count(),2)
        self.assertQuerysetEqual(self.matrix_A.get_columns(), [repr(x_coordinate_1), repr(x_coordinate_2)], ordered=False)


        y_coordinate_1 = {'ycoordinate': 0}
        y_coordinate_2 = {'ycoordinate': 1}

        self.assertEqual(self.matrix_B.get_row_count(),2)
        self.assertQuerysetEqual(self.matrix_B.get_rows(), [repr(y_coordinate_1), repr(y_coordinate_2)], ordered=False)

        self.assertEqual(self.matrix_C.get_matrix(), [[self.cell_1_1_C, self.cell_2_1_C], [self.cell_1_2_C, self.cell_2_2_C]])




    def tearDown(self):

        self.get_blog.delete()
        self.post_blog.delete()
        self.blog_comments.delete()
        self.blog_comment_post.delete()
        self.blog_delete.delete()

        self.protocol.delete()

        self.admin.delete()

        self.matrix_owner.delete()
        self.matrix_not_owner.delete()

        self.cell_1_A.delete()
        self.cell_2_A.delete()
        self.matrix_A.delete()

        self.cell_1_B.delete()
        self.cell_2_B.delete()
        self.matrix_B.delete()

        self.cell_1_1_C.delete()
        self.cell_1_2_C.delete()
        self.cell_2_1_C.delete()
        self.cell_2_2_C.delete()
        self.matrix_C.delete()

        self.image_type.delete()
        self.image_server.delete()

        self.image.delete()

        self.credential.delete()

        self.owner.delete()


class ProfileTest(TestCase):

    def setUp(self):

        self.user = User.objects.create(username="fbloggs69", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())

    def test_profile_creation(self):

        w = Profile(self, bio="profile_bio", location="profile_location", birth_date=timezone.now(), email_confirmed=True, user=self.user )

        self.assertTrue(isinstance(w, Profile))

        self.assertEqual(w.__str__(), str(w.id) + ", " + w.bio + ", " + w.location + ", " + str(w.birth_date) + ", " + str(w.email_confirmed))
        self.assertEqual(w.__unicode__(), str(w.id) + ", " + str(w.user.id) + ", " + w.bio + ", " + w.location + ", " + str(w.birth_date) + ", " + str(w.email_confirmed))

    def tearDown(self):

        self.user.delete()


class TypeTest(TestCase):

    def setUp(self):

        self.type_owner = User.objects.create(username="fbloggs69", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.type_not_owner = User.objects.create(username="fbloggs96", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())

    def test_type_creation(self):

        ordinary_type = Type(name="ordinary_type", owner=self.type_owner)

        self.assertTrue(isinstance(ordinary_type, Type))

        self.assertEqual(ordinary_type.__str__(), ordinary_type.name)
        self.assertEqual(ordinary_type.__unicode__(), str(ordinary_type.id) + ", " + ordinary_type.name + ", " + str(ordinary_type.owner.id))

        self.assertEqual(ordinary_type.is_owned_by(self.type_owner),True)
        self.assertEqual(ordinary_type.is_owned_by(self.type_not_owner),False)

        ordinary_type.set_owner(self.type_not_owner)

        self.assertEqual(ordinary_type.is_owned_by(self.type_owner),False)
        self.assertEqual(ordinary_type.is_owned_by(self.type_not_owner),True)

    def tearDown(self):

        self.type_owner.delete()
        self.type_not_owner.delete()


class ProtocolTest(TestCase):

    def setUp(self):

        self.protocol_owner = User.objects.create(username="fbloggs69", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.protocol_not_owner = User.objects.create(username="fbloggs96", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())

    def test_protocol_creation(self):

        ordinary_type = Protocol(name="ordinary_protocol", owner=self.protocol_owner)

        self.assertTrue(isinstance(ordinary_type, Protocol))

        self.assertEqual(ordinary_type.__str__(), ordinary_type.name)
        self.assertEqual(ordinary_type.__unicode__(), str(ordinary_type.id) + ", " + ordinary_type.name + ", " + str(ordinary_type.owner.id))

        self.assertEqual(ordinary_type.is_owned_by(self.protocol_owner),True)
        self.assertEqual(ordinary_type.is_owned_by(self.protocol_not_owner),False)

        ordinary_type.set_owner(self.protocol_not_owner)

        self.assertEqual(ordinary_type.is_owned_by(self.protocol_owner),False)
        self.assertEqual(ordinary_type.is_owned_by(self.protocol_not_owner),True)

    def tearDown(self):

        self.protocol_owner.delete()
        self.protocol_not_owner.delete()


class ServerTest(TestCase):

    def setUp(self):

        self.server_owner = User.objects.create(username="fbloggs69", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.server_not_owner = User.objects.create(username="fbloggs96", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.server_type = Type.objects.create(name="type_name", owner=self.server_owner)

    def test_server_creation(self):

        ordinary_server = Server(name="server_name", url="server_url", uid="server_uid", pwd="server_pwd", type=self.server_type, owner=self.server_owner)

        self.assertTrue(isinstance(ordinary_server, Server))

        self.assertEqual(ordinary_server.__str__(), str(ordinary_server.id) + ", " + ordinary_server.name + ", " + ordinary_server.url + ", " + ordinary_server.uid + ", " + ordinary_server.pwd + ", " + str(ordinary_server.type.id) + ", " + str(ordinary_server.owner.id))
        self.assertEqual(ordinary_server.__unicode__(), str(ordinary_server.id) + ", " + ordinary_server.name + ", " + ordinary_server.url + ", " + ordinary_server.uid + ", " + ordinary_server.pwd + ", " + str(ordinary_server.type.id) + ", " + str(ordinary_server.owner.id))

        self.assertEqual(ordinary_server.is_owned_by(self.server_owner),True)
        self.assertEqual(ordinary_server.is_owned_by(self.server_not_owner),False)

        ordinary_server.set_owner(self.server_not_owner)

        self.assertEqual(ordinary_server.is_owned_by(self.server_owner),False)
        self.assertEqual(ordinary_server.is_owned_by(self.server_not_owner),True)

        ordinary_server.set_pwd("87654321")

        self.assertEqual(ordinary_server.pwd, "87654321")

    def tearDown(self):
        self.server_owner.delete()
        self.server_not_owner.delete()
        self.server_type.delete()


class CommandTest(TestCase):

    def setUp(self):

        self.command_owner = User.objects.create(username="fbloggs69", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.command_not_owner = User.objects.create(username="fbloggs96", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.command_type = Type.objects.create(name="type_name", owner=self.command_owner)
        self.command_protocol = Protocol.objects.create(name="protocol_nam", owner=self.command_owner)

    def test_command_creation(self):

        ordinary_command = Command(name="ordinary_command", application="command_application", preamble="command_preamble", postamble="command_postamble", protocol=self.command_protocol, type=self.command_type, owner=self.command_owner)

        self.assertTrue(isinstance(ordinary_command, Command))

        self.assertEqual(ordinary_command.__str__(), str(ordinary_command.id) + ", " +  ordinary_command.name + ", " +  ordinary_command.application + ", " +  ordinary_command.preamble + ", " +  ordinary_command.postamble + ", " +  str(ordinary_command.protocol.id) + ", " +  str(ordinary_command.type.id) + ", " +  str(ordinary_command.owner.id))
        self.assertEqual(ordinary_command.__unicode__(), str(ordinary_command.id) + ", " +  ordinary_command.name + ", " +  ordinary_command.application + ", " +  ordinary_command.preamble + ", " +  ordinary_command.postamble + ", " +  str(ordinary_command.protocol.id) + ", " +  str(ordinary_command.type.id) + ", " +  str(ordinary_command.owner.id))

        self.assertEqual(ordinary_command.is_owned_by(self.command_owner),True)
        self.assertEqual(ordinary_command.is_owned_by(self.command_not_owner),False)

        ordinary_command.set_owner(self.command_not_owner)

        self.assertEqual(ordinary_command.is_owned_by(self.command_owner),False)
        self.assertEqual(ordinary_command.is_owned_by(self.command_not_owner),True)

    def tearDown(self):

        self.command_owner.delete()
        self.command_not_owner.delete()
        self.command_type.delete()
        self.command_protocol.delete()


class ImageTest(TestCase):

    def setUp(self):

        self.image_owner = User.objects.create(username="fbloggs69", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.image_not_owner = User.objects.create(username="fbloggs96", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.image_type = Type.objects.create(name="type_name", owner=self.image_owner)
        self.image_server = Server.objects.create(name="server_name", url="server_url", uid="server_uid", pwd="server_pwd", type=self.image_type, owner=self.image_owner)

    def test_image_creation(self):

        ordinary_image = Image(identifier=0, name="image_name", server=self.image_server, viewer_url="image_viewer_url", birdseye_url="image_birdseye_url", owner=self.image_owner, active=True, roi=1)

        self.assertTrue(isinstance(ordinary_image, Image))

        self.assertEqual(ordinary_image.__str__(), str(ordinary_image.id) + ", " + str(ordinary_image.identifier) + ", " + ordinary_image.name + ", " + str(ordinary_image.server.id) + ", " + ordinary_image.viewer_url + ", " + ordinary_image.birdseye_url + ", " + str(ordinary_image.owner.id) + ", " + str(ordinary_image.active) + ", " + str(ordinary_image.roi))
        self.assertEqual(ordinary_image.__unicode__(), str(ordinary_image.id) + ", " + str(ordinary_image.identifier) + ", " + ordinary_image.name + ", " + str(ordinary_image.server.id) + ", " + ordinary_image.viewer_url + ", " + ordinary_image.birdseye_url + ", " + str(ordinary_image.owner.id) + ", " + str(ordinary_image.active) + ", " + str(ordinary_image.roi))

        self.assertEqual(ordinary_image.is_owned_by(self.image_owner),True)
        self.assertEqual(ordinary_image.is_owned_by(self.image_not_owner),False)

        ordinary_image.set_owner(self.image_not_owner)

        self.assertEqual(ordinary_image.is_owned_by(self.image_owner),False)
        self.assertEqual(ordinary_image.is_owned_by(self.image_not_owner),True)

        ordinary_image.set_inactive()

        self.assertEqual(ordinary_image.is_active(),False)
        self.assertEqual(ordinary_image.is_inactive(),True)

        ordinary_image.set_active()

        self.assertEqual(ordinary_image.is_active(),True)
        self.assertEqual(ordinary_image.is_inactive(),False)

    def tearDown(self):

        self.image_owner.delete()
        self.image_not_owner.delete()
        self.image_type.delete()
        self.image_server.delete()


class CellTest(TestCase):

    def setUp(self):

        self.owner = User.objects.create(username="fbloggs69", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.matrix = Matrix.objects.create(title="matrix_title", description="matrix_description", blogpost="matrix_blogpost", created=timezone.now(), modified=timezone.now(), height=100, width=100, owner=self.owner )
        self.matrix_other = Matrix.objects.create(title="matrix_title", description="matrix_description", blogpost="matrix_blogpost", created=timezone.now(), modified=timezone.now(), height=100, width=100, owner=self.owner )

        self.type = Type.objects.create(name="type_name", owner=self.owner)
        self.server = Server.objects.create(name="server_name", url="server_url", uid="server_uid", pwd="server_pwd", type=self.type, owner=self.owner)
        self.image = Image(id=0, identifier=0, name="image_name", server=self.server, viewer_url="image_viewer_url", birdseye_url="image_birdseye_url", owner=self.owner, active=True, roi=1)

    def test_cell_creation(self):

        ordinary_cell = Cell(matrix=self.matrix, title="ordinary_cell", description="cell_description", xcoordinate=99, ycoordinate=99, blogpost="cell_blogpost", image=self.image)
        master_cell = Cell(matrix=self.matrix, title="master_cell", description="master_cell", xcoordinate=0, ycoordinate=0, blogpost="cell_blogpost", image=self.image)
        row_header_cell = Cell(matrix=self.matrix, title="row_header_cell", description="master_cell", xcoordinate=99, ycoordinate=0, blogpost="cell_blogpost", image=self.image)
        column_header_cell = Cell(matrix=self.matrix, title="column_header_cell", description="master_cell", xcoordinate=0, ycoordinate=99, blogpost="cell_blogpost", image=self.image)
        ordinary_cell_no_blogpost = Cell(matrix=self.matrix, title="ordinary_cell_no_blogpost", description="cell_description", xcoordinate=99, ycoordinate=99, blogpost="", image=self.image)
        ordinary_cell_no_image = Cell(matrix=self.matrix, title="ordinary_cell_no_image", description="cell_description", xcoordinate=99, ycoordinate=99, blogpost="", image=None)

        self.assertTrue(isinstance(ordinary_cell, Cell))

        self.assertEqual(ordinary_cell.__unicode__(), str(ordinary_cell.id) + ", " + str(ordinary_cell.matrix.id) + ", " + ordinary_cell.title + ", " + ordinary_cell.description + ", " + str(ordinary_cell.xcoordinate) + ", " + str(ordinary_cell.ycoordinate) + ", " + ordinary_cell.blogpost + ", " + str(ordinary_cell.image.id))
        self.assertEqual(ordinary_cell.__str__(), str(ordinary_cell.id) + ", " + str(ordinary_cell.matrix.id) + ", " + ordinary_cell.title + ", " + ordinary_cell.description + ", " + str(ordinary_cell.xcoordinate) + ", " + str(ordinary_cell.ycoordinate) + ", " + ordinary_cell.blogpost + ", " + str(ordinary_cell.image.id))

        self.assertEqual(ordinary_cell.is_master(),False)
        self.assertEqual(master_cell.is_master(),True)
        self.assertEqual(row_header_cell.is_master(),False)
        self.assertEqual(column_header_cell.is_master(),False)

        self.assertEqual(ordinary_cell.is_header(),False)
        self.assertEqual(master_cell.is_header(),True)
        self.assertEqual(row_header_cell.is_header(),True)
        self.assertEqual(column_header_cell.is_header(),True)

        self.assertEqual(ordinary_cell.is_column_header(),False)
        self.assertEqual(master_cell.is_column_header(),True)
        self.assertEqual(row_header_cell.is_column_header(),False)
        self.assertEqual(column_header_cell.is_column_header(),True)

        self.assertEqual(ordinary_cell.is_row_header(),False)
        self.assertEqual(master_cell.is_row_header(),True)
        self.assertEqual(row_header_cell.is_row_header(),True)
        self.assertEqual(column_header_cell.is_row_header(),False)

        self.assertEqual(ordinary_cell.has_no_blogpost(),False)
        self.assertEqual(ordinary_cell_no_blogpost.has_no_blogpost(),True)

        self.assertEqual(ordinary_cell.has_blogpost(),True)
        self.assertEqual(ordinary_cell_no_blogpost.has_blogpost(),False)

        ordinary_cell.set_blogpost("")
        ordinary_cell_no_blogpost.set_blogpost("87654321")

        self.assertEqual(ordinary_cell.has_no_blogpost(),True)
        self.assertEqual(ordinary_cell_no_blogpost.has_no_blogpost(),False)

        self.assertEqual(ordinary_cell.has_blogpost(),False)
        self.assertEqual(ordinary_cell_no_blogpost.has_blogpost(),True)

        self.assertEqual(ordinary_cell.has_no_image(),False)
        self.assertEqual(ordinary_cell_no_image.has_no_image(),True)
        self.assertEqual(ordinary_cell_no_image.__str__(), str(ordinary_cell_no_image.id) + ", " + str(ordinary_cell_no_image.matrix.id) + ", " + ordinary_cell_no_image.title + ", " + ordinary_cell_no_image.description + ", " + str(ordinary_cell_no_image.xcoordinate) + ", " + str(ordinary_cell_no_image.ycoordinate) + ", " + ordinary_cell_no_image.blogpost + ", " + "None")

        self.assertEqual(ordinary_cell.has_image(),True)
        self.assertEqual(ordinary_cell_no_image.has_image(),False)

        ordinary_cell.set_matrix(self.matrix_other)

        self.assertEqual(ordinary_cell.matrix,self.matrix_other)

        ordinary_cell.increment_x()
        self.assertEqual(ordinary_cell.xcoordinate,100)

        ordinary_cell.increment_y()
        self.assertEqual(ordinary_cell.ycoordinate,100)

        ordinary_cell.decrement_x()
        self.assertEqual(ordinary_cell.xcoordinate,99)

        ordinary_cell.decrement_y()
        self.assertEqual(ordinary_cell.ycoordinate,99)

    def tearDown(self):

        self.image.delete()
        self.matrix.delete()
        self.matrix_other.delete()
        self.type.delete()
        self.server.delete()
        self.owner.delete()


class BlogTest(TestCase):

    def setUp(self):

        self.blog_owner = User.objects.create(username="fbloggs69", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.blog_not_owner = User.objects.create(username="fbloggs96", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.blog_protocol = Protocol.objects.create(name="protocol_nam", owner=self.blog_owner)

    def test_blog_creation(self):

        ordinary_blog = Blog(name="ordinary_blog", application="blog_application", preamble="blog_preamble", postamble="blog_postamble", protocol=self.blog_protocol, url="blog_url", owner=self.blog_owner)

        self.assertTrue(isinstance(ordinary_blog, Blog))

        self.assertEqual(ordinary_blog.__str__(), str(ordinary_blog.id) + ", " +  ordinary_blog.name + ", " +  str(ordinary_blog.protocol.id) + ", " +  str(ordinary_blog.url) + ", " +  ordinary_blog.application + ", " +  ordinary_blog.preamble + ", " +  ordinary_blog.postamble + ", " +  str(ordinary_blog.owner.id))
        self.assertEqual(ordinary_blog.__unicode__(), str(ordinary_blog.id) + ", " +  ordinary_blog.name + ", " +  str(ordinary_blog.protocol.id) + ", " +  str(ordinary_blog.url) + ", " +  ordinary_blog.application + ", " +  ordinary_blog.preamble + ", " +  ordinary_blog.postamble + ", " +  str(ordinary_blog.owner.id))

        self.assertEqual(ordinary_blog.is_owned_by(self.blog_owner),True)
        self.assertEqual(ordinary_blog.is_owned_by(self.blog_not_owner),False)

        ordinary_blog.set_owner(self.blog_not_owner)

        self.assertEqual(ordinary_blog.is_owned_by(self.blog_owner),False)
        self.assertEqual(ordinary_blog.is_owned_by(self.blog_not_owner),True)

    def tearDown(self):

        self.blog_owner.delete()
        self.blog_not_owner.delete()
        self.blog_protocol.delete()


class CredentialTest(TestCase):

    def setUp(self):

        self.credential_owner = User.objects.create(username="fbloggs69", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.credential_not_owner = User.objects.create(username="fbloggs96", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())

    def test_credential_creation(self):

        ordinary_credential = Credential(username="credential_username", wordpress=0, apppwd="credential_apppwd", owner=self.credential_owner)
        ordinary_credential_no_apppwd = Credential(username="credential_username", wordpress=0, apppwd="", owner=self.credential_owner)

        self.assertTrue(isinstance(ordinary_credential, Credential))

        self.assertEqual(ordinary_credential.__unicode__(), str(ordinary_credential.id) + ", " + ordinary_credential.username + ", " + str(ordinary_credential.wordpress) + ", " + ordinary_credential.apppwd + ", " + str(ordinary_credential.owner.id))
        self.assertEqual(ordinary_credential.__str__(), str(ordinary_credential.id) + ", " + ordinary_credential.username + ", " + str(ordinary_credential.wordpress) + ", " + ordinary_credential.apppwd + ", " + str(ordinary_credential.owner.id))

        self.assertEqual(ordinary_credential.has_no_apppwd(),False)
        self.assertEqual(ordinary_credential_no_apppwd.has_no_apppwd(),True)

        self.assertEqual(ordinary_credential.has_apppwd(),True)
        self.assertEqual(ordinary_credential_no_apppwd.has_apppwd(),False)

        self.assertEqual(ordinary_credential.is_owned_by(self.credential_owner),True)
        self.assertEqual(ordinary_credential.is_owned_by(self.credential_not_owner),False)

        ordinary_credential.set_owner(self.credential_not_owner)

        self.assertEqual(ordinary_credential.is_owned_by(self.credential_owner),False)
        self.assertEqual(ordinary_credential.is_owned_by(self.credential_not_owner),True)

    def tearDown(self):

        self.credential_owner.delete()
        self.credential_not_owner.delete()
