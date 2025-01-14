from django.test import TestCase
from matrices.models.collectionsummary import CollectionSummary


class CollectionSummaryTestCase(TestCase):

    def setUp(self):
        self.collection = CollectionSummary(
            collection_id=1,
            collection_title="Test Collection",
            collection_description="This is a test collection.",
            collection_owner="Owner",
            collection_image_count=10,
            collection_locked=False,
            collection_authorisation_id=1,
            collection_authorisation_permitted="Permitted",
            collection_authorisation_authority="Authority"
        )

    def test_collection_summary_str(self):
        expected_str = "1, Test Collection, This is a test collection., Owner, This is a test collection., 10, False, Permitted, Authority"
        self.assertEqual(str(self.collection), expected_str)

    def test_collection_summary_repr(self):
        expected_repr = "1, Test Collection, This is a test collection., Owner, This is a test collection., 10, False, Permitted, Authority"
        self.assertEqual(repr(self.collection), expected_repr)

    def test_is_locked(self):
        self.assertFalse(self.collection.is_locked())
        self.collection.collection_locked = True
        self.assertTrue(self.collection.is_locked())

    def test_is_not_locked(self):
        self.assertTrue(self.collection.is_not_locked())
        self.collection.collection_locked = True
        self.assertFalse(self.collection.is_not_locked())

    def test_is_unlocked(self):
        self.assertTrue(self.collection.is_unlocked())
        self.collection.collection_locked = True
        self.assertFalse(self.collection.is_unlocked())

    def test_is_not_unlocked(self):
        self.assertFalse(self.collection.is_not_unlocked())
        self.collection.collection_locked = True
        self.assertTrue(self.collection.is_not_unlocked())

    def test_get_formatted_id(self):
        self.assertEqual(self.collection.get_formatted_id(), "000001")
        self.collection.collection_id = 123
        self.assertEqual(self.collection.get_formatted_id(), "000123")