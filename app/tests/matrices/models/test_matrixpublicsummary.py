from django.test import TestCase
from django.utils import timezone
from matrices.models import MatrixPublicSummary


class MatrixPublicSummaryTestCase(TestCase):

    def setUp(self):
        self.matrix_public_summary = MatrixPublicSummary.objects.create(
            matrix_public_id=1,
            matrix_public_title="Test Title",
            matrix_public_description="Test Description",
            matrix_public_blogpost="Test Blogpost",
            matrix_public_created=timezone.now(),
            matrix_public_modified=timezone.now(),
            matrix_public_height=100,
            matrix_public_width=200,
            matrix_public_owner="Test Owner",
            matrix_public_public=True,
            matrix_public_locked=False
        )

    def test_matrix_public_summary_creation(self):
        self.assertEqual(self.matrix_public_summary.matrix_public_id, 1)
        self.assertEqual(self.matrix_public_summary.matrix_public_title, "Test Title")
        self.assertEqual(self.matrix_public_summary.matrix_public_description, "Test Description")
        self.assertEqual(self.matrix_public_summary.matrix_public_blogpost, "Test Blogpost")
        self.assertEqual(self.matrix_public_summary.matrix_public_height, 100)
        self.assertEqual(self.matrix_public_summary.matrix_public_width, 200)
        self.assertEqual(self.matrix_public_summary.matrix_public_owner, "Test Owner")
        self.assertTrue(self.matrix_public_summary.matrix_public_public)
        self.assertFalse(self.matrix_public_summary.matrix_public_locked)

    def test_get_formatted_id(self):
        formatted_id = self.matrix_public_summary.get_formatted_id()
        self.assertEqual(formatted_id, "CPW:000001")

    def test_str_method(self):
        expected_str = f"1, Test Title, Test Description, Test Blogpost, {self.matrix_public_summary.matrix_public_created}, {self.matrix_public_summary.matrix_public_modified}, 100, 200, Test Owner, True, False"
        self.assertEqual(str(self.matrix_public_summary), expected_str)

    def test_repr_method(self):
        expected_repr = f"1, Test Title, Test Description, Test Blogpost, {self.matrix_public_summary.matrix_public_created}, {self.matrix_public_summary.matrix_public_modified}, 100, 200, Test Owner, True, False"
        self.assertEqual(repr(self.matrix_public_summary), expected_repr)

    def test_get_or_none(self):
        obj = MatrixPublicSummary.objects.get_or_none(matrix_public_id=1)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.matrix_public_id, 1)

        obj_none = MatrixPublicSummary.objects.get_or_none(matrix_public_id=999)
        self.assertIsNone(obj_none)