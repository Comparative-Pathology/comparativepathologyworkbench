import unittest
from unittest.mock import MagicMock
from matrices.routines.exists_collection_for_image import exists_collection_for_image


class TestExistsCollectionForImage(unittest.TestCase):

    def test_collection_exists(self):
        # Mock collection and image
        mock_collection = MagicMock()
        mock_image = MagicMock()
        mock_image.collections.all.return_value = [mock_collection]

        # Test when collection exists in image
        result = exists_collection_for_image(mock_collection, mock_image)
        self.assertTrue(result)

    def test_collection_does_not_exist(self):
        # Mock collection and image
        mock_collection = MagicMock()
        mock_image = MagicMock()
        mock_image.collections.all.return_value = []

        # Test when collection does not exist in image
        result = exists_collection_for_image(mock_collection, mock_image)
        self.assertFalse(result)

    def test_collection_not_in_list(self):
        # Mock collections and image
        mock_collection = MagicMock()
        mock_collection_2 = MagicMock()
        mock_image = MagicMock()
        mock_image.collections.all.return_value = [mock_collection_2]

        # Test when collection is not in the list of image collections
        result = exists_collection_for_image(mock_collection, mock_image)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
# The test case above is a unit test for the exists_collection_for_image function.
