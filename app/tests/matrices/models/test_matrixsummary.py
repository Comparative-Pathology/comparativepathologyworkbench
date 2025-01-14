from django.test import TestCase
from django.utils import timezone
from matrices.models import MatrixSummary


class MatrixSummaryTestCase(TestCase):

    def setUp(self):
        self.matrix_summary = MatrixSummary.objects.create(
            matrix_id=1,
            matrix_title="Test Matrix",
            matrix_description="This is a test matrix.",
            matrix_blogpost="Test Blogpost",
            matrix_created=timezone.now(),
            matrix_modified=timezone.now(),
            matrix_height=10,
            matrix_width=10,
            matrix_owner="Test Owner",
            matrix_public=True,
            matrix_locked=False,
            matrix_authorisation_id=1,
            matrix_authorisation_permitted="Permitted",
            matrix_authorisation_authority="Authority"
        )

    def test_matrix_summary_str(self):
        expected_str = f"{self.matrix_summary.matrix_id}, \
            {self.matrix_summary.matrix_title}, \
            {self.matrix_summary.matrix_description}, \
            {self.matrix_summary.matrix_blogpost}, \
            {self.matrix_summary.matrix_created}, \
            {self.matrix_summary.matrix_modified}, \
            {self.matrix_summary.matrix_height}, \
            {self.matrix_summary.matrix_width}, \
            {self.matrix_summary.matrix_owner}, \
            {self.matrix_summary.matrix_public}, \
            {self.matrix_summary.matrix_locked}, \
            {self.matrix_summary.matrix_authorisation_id}, \
            {self.matrix_summary.matrix_authorisation_permitted}, \
            {self.matrix_summary.matrix_authorisation_authority}"
        self.assertEqual(str(self.matrix_summary), expected_str)

    def test_matrix_summary_repr(self):
        expected_repr = f"{self.matrix_summary.matrix_id}, \
            {self.matrix_summary.matrix_title}, \
            {self.matrix_summary.matrix_description}, \
            {self.matrix_summary.matrix_blogpost}, \
            {self.matrix_summary.matrix_created}, \
            {self.matrix_summary.matrix_modified}, \
            {self.matrix_summary.matrix_height}, \
            {self.matrix_summary.matrix_width}, \
            {self.matrix_summary.matrix_owner}, \
            {self.matrix_summary.matrix_public}, \
            {self.matrix_summary.matrix_locked}, \
            {self.matrix_summary.matrix_authorisation_id}, \
            {self.matrix_summary.matrix_authorisation_permitted}, \
            {self.matrix_summary.matrix_authorisation_authority}"
        self.assertEqual(repr(self.matrix_summary), expected_repr)

    def test_is_locked(self):
        self.assertFalse(self.matrix_summary.is_locked())

    def test_is_not_locked(self):
        self.assertTrue(self.matrix_summary.is_not_locked())

    def test_is_public(self):
        self.assertTrue(self.matrix_summary.is_public())

    def test_is_not_public(self):
        self.assertFalse(self.matrix_summary.is_not_public())

    def test_is_unlocked(self):
        self.assertTrue(self.matrix_summary.is_unlocked())

    def test_is_not_unlocked(self):
        self.assertFalse(self.matrix_summary.is_not_unlocked())

    def test_is_private(self):
        self.assertFalse(self.matrix_summary.is_private())

    def test_is_not_private(self):
        self.assertTrue(self.matrix_summary.is_not_private())

    def test_get_formatted_id(self):
        self.assertEqual(self.matrix_summary.get_formatted_id(), "CPW:000001")