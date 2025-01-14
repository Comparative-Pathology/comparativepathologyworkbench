from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Collection, Image, CollectionImageOrder


class CollectionImageOrderTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.collection = Collection.objects.create(name='Test Collection')
        self.image = Image.objects.create(name='Test Image')
        self.collection_image_order = CollectionImageOrder.objects.create(
            collection=self.collection,
            image=self.image,
            permitted=self.user,
            ordering=1
        )

    def test_create_collection_image_order(self):
        self.assertEqual(self.collection_image_order.collection, self.collection)
        self.assertEqual(self.collection_image_order.image, self.image)
        self.assertEqual(self.collection_image_order.permitted, self.user)
        self.assertEqual(self.collection_image_order.ordering, 1)

    def test_str_representation(self):
        self.assertEqual(str(self.collection_image_order), f"{self.collection_image_order.id}, {self.collection.id}, {self.image.id}, {self.user.id}, 1")

    def test_repr_representation(self):
        self.assertEqual(repr(self.collection_image_order), f"{self.collection_image_order.id}, {self.collection.id}, {self.image.id}, {self.user.id}, 1")

    def test_set_collection(self):
        new_collection = Collection.objects.create(name='New Collection')
        self.collection_image_order.set_collection(new_collection)
        self.assertEqual(self.collection_image_order.collection, new_collection)

    def test_set_image(self):
        new_image = Image.objects.create(name='New Image')
        self.collection_image_order.set_image(new_image)
        self.assertEqual(self.collection_image_order.image, new_image)

    def test_set_permitted(self):
        new_user = User.objects.create(username='newuser')
        self.collection_image_order.set_permitted(new_user)
        self.assertEqual(self.collection_image_order.permitted, new_user)

    def test_set_ordering(self):
        self.collection_image_order.set_ordering(2)
        self.assertEqual(self.collection_image_order.ordering, 2)

    def test_is_collection(self):
        self.assertTrue(self.collection_image_order.is_collection(self.collection))
        new_collection = Collection.objects.create(name='New Collection')
        self.assertFalse(self.collection_image_order.is_collection(new_collection))

    def test_is_image(self):
        self.assertTrue(self.collection_image_order.is_image(self.image))
        new_image = Image.objects.create(name='New Image')
        self.assertFalse(self.collection_image_order.is_image(new_image))

    def test_is_permitted_by(self):
        self.assertTrue(self.collection_image_order.is_permitted_by(self.user))
        new_user = User.objects.create(username='newuser')
        self.assertFalse(self.collection_image_order.is_permitted_by(new_user))

    def test_decrement_ordering(self):
        self.collection_image_order.decrement_ordering()
        self.assertEqual(self.collection_image_order.ordering, 0)

    def test_increment_ordering(self):
        self.collection_image_order.increment_ordering()
        self.assertEqual(self.collection_image_order.ordering, 2)