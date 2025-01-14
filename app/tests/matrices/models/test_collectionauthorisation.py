from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Collection, CollectionAuthority, CollectionAuthorisation


class CollectionAuthorisationTestCase(TestCase):

    def setUp(self):
        self.collection = Collection.objects.create(name="Test Collection")
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.collection_authority = CollectionAuthority.objects.create(name="Test Authority")
        self.collection_authorisation = CollectionAuthorisation.objects.create(
            collection=self.collection,
            permitted=self.user,
            collection_authority=self.collection_authority
        )

    def test_create_collection_authorisation(self):
        collection_authorisation = CollectionAuthorisation.create(
            collection=self.collection,
            permitted=self.user,
            collection_authority=self.collection_authority
        )
        self.assertIsNotNone(collection_authorisation)
        self.assertEqual(collection_authorisation.collection, self.collection)
        self.assertEqual(collection_authorisation.permitted, self.user)
        self.assertEqual(collection_authorisation.collection_authority, self.collection_authority)

    def test_str_representation(self):
        expected_str = f"{self.collection_authorisation.id}, {self.collection.id}, {self.user.id}, {self.collection_authority.id}"
        self.assertEqual(str(self.collection_authorisation), expected_str)

    def test_set_collection(self):
        new_collection = Collection.objects.create(name="New Collection")
        self.collection_authorisation.set_collection(new_collection)
        self.assertEqual(self.collection_authorisation.collection, new_collection)

    def test_set_permitted(self):
        new_user = User.objects.create_user(username='newuser', password='12345')
        self.collection_authorisation.set_permitted(new_user)
        self.assertEqual(self.collection_authorisation.permitted, new_user)

    def test_set_collection_authority(self):
        new_collection_authority = CollectionAuthority.objects.create(name="New Authority")
        self.collection_authorisation.set_collection_authority(new_collection_authority)
        self.assertEqual(self.collection_authorisation.collection_authority, new_collection_authority)

    def test_is_collection(self):
        self.assertTrue(self.collection_authorisation.is_collection(self.collection))
        new_collection = Collection.objects.create(name="New Collection")
        self.assertFalse(self.collection_authorisation.is_collection(new_collection))

    def test_is_permitted_by(self):
        self.assertTrue(self.collection_authorisation.is_permitted_by(self.user))
        new_user = User.objects.create_user(username='newuser', password='12345')
        self.assertFalse(self.collection_authorisation.is_permitted_by(new_user))

    def test_is_collection_authority(self):
        self.assertTrue(self.collection_authorisation.is_collection_authority(self.collection_authority))
        new_collection_authority = CollectionAuthority.objects.create(name="New Authority")
        self.assertFalse(self.collection_authorisation.is_collection_authority(new_collection_authority))