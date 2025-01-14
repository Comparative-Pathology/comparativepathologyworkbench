import unittest
from unittest.mock import patch, MagicMock
from matrices.models import Server


class TestServer(unittest.TestCase):

    def setUp(self):
        self.server = Server(
            name="Test Server",
            url_server="testserver.com",
            uid="testuser",
            pwd="testpassword",
            type=MagicMock(id=1, name="WORDPRESS"),
            owner=MagicMock(id=1),
            accessible=True
        )

    def test_get_uid_and_url(self):
        expected_result = "testuser@testserver.com"
        self.assertEqual(self.server.get_uid_and_url(), expected_result)

    @patch('requests.get')
    def test_get_wordpress_json(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'id': 1,
            'title': {'rendered': 'Test Image'},
            'source_url': 'http://testserver.com/image.jpg',
            'media_details': {
                'sizes': {
                    'thumbnail': {'source_url': 'http://testserver.com/thumbnail.jpg'},
                    'medium': {'source_url': 'http://testserver.com/medium.jpg'}
                }
            }
        }]
        mock_get.return_value = mock_response

        credential = MagicMock(username="testuser", apppwd="testapppwd", wordpress="wordpress")
        page_id = 1

        result = self.server.get_wordpress_json(credential, page_id)
        self.assertIn('images', result)
        self.assertEqual(len(result['images']), 1)
        self.assertEqual(result['images'][0]['name'], 'Test Image')

    @patch('requests.get')
    def test_get_wordpress_image_json(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'caption': {'rendered': 'Test Caption'},
            'title': {'rendered': 'Test Image'},
            'alt_text': 'Test Description',
            'source_url': 'http://testserver.com/image.jpg',
            'media_details': {
                'sizes': {
                    'thumbnail': {'source_url': 'http://testserver.com/thumbnail.jpg'},
                    'medium': {'source_url': 'http://testserver.com/medium.jpg'}
                }
            }
        }
        mock_get.return_value = mock_response

        credential = MagicMock(username="testuser", apppwd="testapppwd")
        image_id = 1

        result = self.server.get_wordpress_image_json(credential, image_id)
        self.assertIn('image', result)
        self.assertEqual(result['image']['name'], 'Test Image')
        self.assertEqual(result['image']['caption'], 'Test Caption')


if __name__ == '__main__':
    unittest.main()