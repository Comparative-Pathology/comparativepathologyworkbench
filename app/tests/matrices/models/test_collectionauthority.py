from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models.collectionauthority import CollectionAuthority, AUTHORITY_NONE, AUTHORITY_VIEWER, AUTHORITY_OWNER, AUTHORITY_ADMIN


class CollectionAuthorityTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.collection_authority = CollectionAuthority.create(name=AUTHORITY_OWNER, owner=self.user)

    def test_create_collection_authority(self):
        self.assertEqual(self.collection_authority.name, AUTHORITY_OWNER)
        self.assertEqual(self.collection_authority.owner, self.user)

    def test_str_representation(self):
        self.assertEqual(str(self.collection_authority), AUTHORITY_OWNER)

    def test_repr_representation(self):
        self.assertEqual(repr(self.collection_authority), f"{self.collection_authority.id}, {AUTHORITY_OWNER}, {self.user.id}")

    def test_is_owned_by(self):
        self.assertTrue(self.collection_authority.is_owned_by(self.user))
        another_user = User.objects.create(username='anotheruser')
        self.assertFalse(self.collection_authority.is_owned_by(another_user))

    def test_set_owner(self):
        another_user = User.objects.create(username='anotheruser')
        self.collection_authority.set_owner(another_user)
        self.assertEqual(self.collection_authority.owner, another_user)

    def test_set_as_none(self):
        self.collection_authority.set_as_none()
        self.assertEqual(self.collection_authority.name, AUTHORITY_NONE)

    def test_set_as_viewer(self):
        self.collection_authority.set_as_viewer()
        self.assertEqual(self.collection_authority.name, AUTHORITY_VIEWER)

    def test_set_as_owner(self):
        self.collection_authority.set_as_owner()
        self.assertEqual(self.collection_authority.name, AUTHORITY_OWNER)

    def test_set_as_admin(self):
        self.collection_authority.set_as_admin()
        self.assertEqual(self.collection_authority.name, AUTHORITY_ADMIN)

    def test_is_none(self):
        self.collection_authority.set_as_none()
        self.assertTrue(self.collection_authority.is_none())
        self.assertFalse(self.collection_authority.is_not_none())

    def test_is_viewer(self):
        self.collection_authority.set_as_viewer()
        self.assertTrue(self.collection_authority.is_viewer())
        self.assertFalse(self.collection_authority.is_not_viewer())

    def test_is_owner(self):
        self.collection_authority.set_as_owner()
        self.assertTrue(self.collection_authority.is_owner())
        self.assertFalse(self.collection_authority.is_not_owner())

    def test_is_admin(self):
        self.collection_authority.set_as_admin()
        self.assertTrue(self.collection_authority.is_admin())
        self.assertFalse(self.collection_authority.is_not_admin())