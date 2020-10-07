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

from matrices.core.forms import CellForm


class CellFormTest(TestCase):

    def setUp(self):

        self.owner = User.objects.create(username="fbloggs69", first_name="Fred", last_name="Bloggs", email="fred.bloggs@gmail.com", password="12345678", is_staff=False, is_active=False, is_superuser=False, last_login=timezone.now(), date_joined=timezone.now())
        self.matrix = Matrix.objects.create(title="matrix_title", description="matrix_description", blogpost="matrix_blogpost", created=timezone.now(), modified=timezone.now(), height=100, width=100, owner=self.owner )
        self.matrix_other = Matrix.objects.create(title="matrix_title", description="matrix_description", blogpost="matrix_blogpost", created=timezone.now(), modified=timezone.now(), height=100, width=100, owner=self.owner )

        self.type = Type.objects.create(name="type_name", owner=self.owner)
        self.server = Server.objects.create(name="server_name", url="server_url", uid="server_uid", pwd="server_pwd", type=self.type, owner=self.owner)
        self.image = Image(id=0, identifier=0, name="image_name", server=self.server, viewer_url="image_viewer_url", birdseye_url="image_birdseye_url", owner=self.owner, active=True, roi=1)


    def test_cell_init(self):

        ordinary_cell = Cell(matrix=self.matrix, title="ordinary_cell", description="cell_description", xcoordinate=99, ycoordinate=99, blogpost="cell_blogpost", image=self.image)
        
        cell_form = CellForm(self.owner.id, ordinary_cell.image.id, "POST", instance=ordinary_cell)

        self.assertTrue(isinstance(cell_form, CellForm))
        
        self.assertEqual(cell_form.label_from_instance(self.image), "image_name<a href=\"image_viewer_url\" target=\"_blank\"><img  style=\"width:256px; height:256px; float: left\" title=\"image_name\" src=\"image_birdseye_url\" ></a>")


    def tearDown(self):
    
        self.image.delete()
        self.matrix.delete()
        self.matrix_other.delete()
        self.type.delete()
        self.server.delete()
        self.owner.delete()

