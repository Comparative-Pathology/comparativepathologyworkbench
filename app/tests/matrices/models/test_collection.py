from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Collection, Image

from taggit.models import Tag


class CollectionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.image1 = Image.objects.create(name='Image1')
        self.image2 = Image.objects.create(name='Image2')
        self.collection = Collection.objects.create(title='Test Collection', description='Test Description', owner=self.user)

    def test_create_collection(self):
        collection = Collection.create(title='New Collection', description='New Description', owner=self.user)
        self.assertEqual(collection.title, 'New Collection')
        self.assertEqual(collection.description, 'New Description')
        self.assertEqual(collection.owner, self.user)

    def test_assign_image(self):
        Collection.assign_image(self.image1, self.collection)
        self.assertIn(self.image1, self.collection.images.all())

    def test_unassign_image(self):
        Collection.assign_image(self.image1, self.collection)
        Collection.unassign_image(self.image1, self.collection)
        self.assertNotIn(self.image1, self.collection.images.all())

    def test_is_owned_by(self):
        self.assertTrue(self.collection.is_owned_by(self.user))
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.assertFalse(self.collection.is_owned_by(another_user))

    def test_is_locked(self):
        self.collection.set_locked()
        self.assertTrue(self.collection.is_locked())
        self.collection.set_unlocked()
        self.assertFalse(self.collection.is_locked())

    def test_is_not_locked(self):
        self.collection.set_unlocked()
        self.assertTrue(self.collection.is_not_locked())
        self.collection.set_locked()
        self.assertFalse(self.collection.is_not_locked())

    def test_get_images(self):
        Collection.assign_image(self.image1, self.collection)
        Collection.assign_image(self.image2, self.collection)
        self.assertIn(self.image1, self.collection.get_images())
        self.assertIn(self.image2, self.collection.get_images())

    def test_get_images_count(self):
        Collection.assign_image(self.image1, self.collection)
        Collection.assign_image(self.image2, self.collection)
        self.assertEqual(self.collection.get_images_count(), 2)

    def test_get_hidden_images(self):
        self.image1.hidden = True
        self.image1.save()
        Collection.assign_image(self.image1, self.collection)
        self.assertIn(self.image1, self.collection.get_hidden_images())

    def test_get_hidden_images_count(self):
        self.image1.hidden = True
        self.image1.save()
        Collection.assign_image(self.image1, self.collection)
        self.assertEqual(self.collection.get_hidden_images_count(), 1)

    def test_get_images_for_tag(self):
        tag = Tag.objects.create(name='Test Tag')
        self.image1.tags.add(tag)
        Collection.assign_image(self.image1, self.collection)
        self.assertIn(self.image1, self.collection.get_images_for_tag(tag))

    def test_get_all_images(self):
        Collection.assign_image(self.image1, self.collection)
        Collection.assign_image(self.image2, self.collection)
        self.assertIn(self.image1, self.collection.get_all_images())
        self.assertIn(self.image2, self.collection.get_all_images())

    def test_get_formatted_id(self):
        self.assertEqual(self.collection.get_formatted_id(), f"{self.collection.id:06d}")