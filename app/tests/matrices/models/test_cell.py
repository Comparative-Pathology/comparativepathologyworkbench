from django.test import TestCase
from matrices.models import Cell, Matrix, Image


class CellModelTest(TestCase):

    def setUp(self):
        self.matrix = Matrix.objects.create(title="Test Matrix")
        self.image = Image.objects.create(name="Test Image")
        self.cell = Cell.objects.create(
            matrix=self.matrix,
            title="Test Cell",
            comment="Test Comment",
            description="Test Description",
            xcoordinate=1,
            ycoordinate=1,
            blogpost="Test Blogpost",
            image=self.image
        )

    def test_create_cell(self):
        cell = Cell.objects.create(
            matrix=self.matrix,
            title="New Cell",
            comment="New Comment",
            description="New Description",
            xcoordinate=2,
            ycoordinate=2,
            blogpost="New Blogpost",
            image=self.image
        )
        self.assertEqual(cell.title, "New Cell")
        self.assertEqual(cell.comment, "New Comment")
        self.assertEqual(cell.description, "New Description")
        self.assertEqual(cell.xcoordinate, 2)
        self.assertEqual(cell.ycoordinate, 2)
        self.assertEqual(cell.blogpost, "New Blogpost")
        self.assertEqual(cell.image, self.image)

    def test_str_method(self):
        expected_str = f"{self.cell.id}, {self.matrix.id}, Test Cell, Test Comment, Test Description, 1, 1, Test Blogpost, {self.image.id}"
        self.assertEqual(str(self.cell), expected_str)

    def test_repr_method(self):
        expected_repr = f"{self.cell.id}, {self.matrix.id}, Test Cell, Test Comment, Test Description, 1, 1, Test Blogpost, {self.image.id}"
        self.assertEqual(repr(self.cell), expected_repr)

    def test_is_header(self):
        self.assertFalse(self.cell.is_header())
        self.cell.xcoordinate = 0
        self.assertTrue(self.cell.is_header())
        self.cell.xcoordinate = 1
        self.cell.ycoordinate = 0
        self.assertTrue(self.cell.is_header())

    def test_is_column_header(self):
        self.assertFalse(self.cell.is_column_header())
        self.cell.xcoordinate = 0
        self.assertTrue(self.cell.is_column_header())

    def test_is_row_header(self):
        self.assertFalse(self.cell.is_row_header())
        self.cell.ycoordinate = 0
        self.assertTrue(self.cell.is_row_header())

    def test_is_master(self):
        self.assertFalse(self.cell.is_master())
        self.cell.xcoordinate = 0
        self.cell.ycoordinate = 0
        self.assertTrue(self.cell.is_master())

    def test_has_no_blogpost(self):
        self.assertFalse(self.cell.has_no_blogpost())
        self.cell.blogpost = ''
        self.assertTrue(self.cell.has_no_blogpost())

    def test_has_blogpost(self):
        self.assertTrue(self.cell.has_blogpost())
        self.cell.blogpost = ''
        self.assertFalse(self.cell.has_blogpost())

    def test_has_no_image(self):
        self.assertFalse(self.cell.has_no_image())
        self.cell.image = None
        self.assertTrue(self.cell.has_no_image())

    def test_has_image(self):
        self.assertTrue(self.cell.has_image())
        self.cell.image = None
        self.assertFalse(self.cell.has_image())

    def test_increment_x(self):
        self.cell.increment_x()
        self.assertEqual(self.cell.xcoordinate, 2)

    def test_increment_y(self):
        self.cell.increment_y()
        self.assertEqual(self.cell.ycoordinate, 2)

    def test_decrement_x(self):
        self.cell.decrement_x()
        self.assertEqual(self.cell.xcoordinate, 0)

    def test_decrement_y(self):
        self.cell.decrement_y()
        self.assertEqual(self.cell.ycoordinate, 0)

    def test_add_to_x(self):
        self.cell.add_to_x(3)
        self.assertEqual(self.cell.xcoordinate, 4)

    def test_add_to_y(self):
        self.cell.add_to_y(3)
        self.assertEqual(self.cell.ycoordinate, 4)

    def test_subtract_from_x(self):
        self.cell.subtract_from_x(1)
        self.assertEqual(self.cell.xcoordinate, 0)

    def test_subtract_from_y(self):
        self.cell.subtract_from_y(1)
        self.assertEqual(self.cell.ycoordinate, 0)

    def test_get_coordinates(self):
        self.assertEqual(self.cell.get_coordinates(), "A1")

    def test_get_formatted_id(self):
        formatted_id = self.cell.get_formatted_id()
        self.assertTrue(formatted_id.startswith(self.matrix.get_formatted_id()))

    def test_get_formatted_bench_id(self):
        formatted_bench_id = self.cell.get_formatted_bench_id()
        self.assertEqual(formatted_bench_id, self.matrix.get_formatted_id())