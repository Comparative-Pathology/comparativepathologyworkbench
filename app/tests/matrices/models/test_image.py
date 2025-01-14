from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Image, Server


class ImageModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.server = Server.objects.create(name='Test Server')
        self.image = Image.objects.create(
            identifier=1,
            name='Test Image',
            server=self.server,
            viewer_url='http://example.com/viewer',
            birdseye_url='http://example.com/birdseye',
            roi=10,
            owner=self.user,
            comment='Test comment',
            hidden=False
        )

    def test_image_creation(self):
        self.assertEqual(self.image.identifier, 1)
        self.assertEqual(self.image.name, 'Test Image')
        self.assertEqual(self.image.server, self.server)
        self.assertEqual(self.image.viewer_url, 'http://example.com/viewer')
        self.assertEqual(self.image.birdseye_url, 'http://example.com/birdseye')
        self.assertEqual(self.image.roi, 10)
        self.assertEqual(self.image.owner, self.user)
        self.assertEqual(self.image.comment, 'Test comment')
        self.assertFalse(self.image.hidden)

    def test_image_str(self):
        expected_str = f"{self.image.id}, {self.image.identifier}, {self.image.name}, {self.image.server.id}, {self.image.viewer_url}, {self.image.birdseye_url}, {self.image.owner.id}, {self.image.roi}, {self.image.comment}, {self.image.hidden}"
        self.assertEqual(str(self.image), expected_str)

    def test_image_repr(self):
        expected_repr = f"{self.image.id}, {self.image.identifier}, {self.image.name}, {self.image.server.id}, {self.image.viewer_url}, {self.image.birdseye_url}, {self.image.owner.id}, {self.image.roi}, {self.image.comment}, {self.image.hidden}"
        self.assertEqual(repr(self.image), expected_repr)

    def test_is_owned_by(self):
        self.assertTrue(self.image.is_owned_by(self.user))
        another_user = User.objects.create(username='anotheruser')
        self.assertFalse(self.image.is_owned_by(another_user))

    def test_is_omero_image(self):
        self.server.is_omero547 = lambda: True
        self.assertTrue(self.image.is_omero_image())
        self.server.is_omero547 = lambda: False
        self.assertFalse(self.image.is_omero_image())

    def test_is_non_omero_image(self):
        self.server.is_omero547 = lambda: True
        self.assertFalse(self.image.is_non_omero_image())
        self.server.is_omero547 = lambda: False
        self.assertTrue(self.image.is_non_omero_image())

    def test_is_duplicate(self):
        duplicate_image = Image(
            identifier=1,
            name='Test Image',
            server=self.server,
            viewer_url='http://example.com/viewer',
            birdseye_url='http://example.com/birdseye',
            roi=10,
            owner=self.user,
            comment='Test comment',
            hidden=False
        )
        self.assertTrue(self.image.is_duplicate(
            duplicate_image.identifier,
            duplicate_image.name,
            duplicate_image.server,
            duplicate_image.viewer_url,
            duplicate_image.birdseye_url,
            duplicate_image.roi,
            duplicate_image.owner,
            duplicate_image.comment,
            duplicate_image.hidden
        ))

    def test_image_id(self):
        self.assertEqual(self.image.image_id(), 1)

    def test_has_tags(self):
        self.assertFalse(self.image.has_tags())
        self.image.tags.add('testtag')
        self.assertTrue(self.image.has_tags())

    def test_get_tags(self):
        self.image.tags.add('testtag')
        tags = self.image.get_tags()
        self.assertEqual(tags.count(), 1)
        self.assertEqual(tags.first().name, 'testtag')

    def test_has_this_tag(self):
        self.image.tags.add('testtag')
        self.assertTrue(self.image.has_this_tag('testtag'))
        self.assertFalse(self.image.has_this_tag('nottesttag'))