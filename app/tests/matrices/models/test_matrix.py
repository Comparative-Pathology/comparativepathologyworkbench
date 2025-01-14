import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Matrix, Collection
from taggit.models import Tag


class MatrixModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.collection = Collection.objects.create(name='Test Collection')
        self.tag = Tag.objects.create(name='Test Tag')
        self.matrix = Matrix.objects.create(
            title='Test Matrix',
            description='Test Description',
            blogpost='12345',
            height=100,
            width=100,
            owner=self.user,
            last_used_collection=self.collection,
            last_used_tag=self.tag,
            public=True,
            locked=False
        )

    def test_matrix_creation(self):
        self.assertEqual(self.matrix.title, 'Test Matrix')
        self.assertEqual(self.matrix.description, 'Test Description')
        self.assertEqual(self.matrix.blogpost, '12345')
        self.assertEqual(self.matrix.height, 100)
        self.assertEqual(self.matrix.width, 100)
        self.assertEqual(self.matrix.owner, self.user)
        self.assertEqual(self.matrix.last_used_collection, self.collection)
        self.assertEqual(self.matrix.last_used_tag, self.tag)
        self.assertTrue(self.matrix.public)
        self.assertFalse(self.matrix.locked)

    def test_matrix_str(self):
        self.assertEqual(str(self.matrix), f"CPW:{self.matrix.id:06d}, Test Matrix")

    def test_matrix_repr(self):
        expected_repr = f"{self.matrix.id}, Test Matrix, Test Description, 12345, {self.matrix.created}, {self.matrix.modified}, 100, 100, {self.user.id}, True, False, {self.collection.id}"
        self.assertEqual(repr(self.matrix), expected_repr)

    def test_matrix_is_owned_by(self):
        self.assertTrue(self.matrix.is_owned_by(self.user))
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.assertFalse(self.matrix.is_owned_by(another_user))

    def test_matrix_set_owner(self):
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.matrix.set_owner(another_user)
        self.assertEqual(self.matrix.owner, another_user)

    def test_matrix_set_blogpost(self):
        self.matrix.set_blogpost('67890')
        self.assertEqual(self.matrix.blogpost, '67890')

    def test_matrix_has_no_blogpost(self):
        self.matrix.set_blogpost('')
        self.assertTrue(self.matrix.has_no_blogpost())
        self.matrix.set_blogpost('0')
        self.assertTrue(self.matrix.has_no_blogpost())

    def test_matrix_has_blogpost(self):
        self.assertTrue(self.matrix.has_blogpost())
        self.matrix.set_blogpost('')
        self.assertFalse(self.matrix.has_blogpost())

    def test_matrix_set_last_used_collection(self):
        new_collection = Collection.objects.create(name='New Collection')
        self.matrix.set_last_used_collection(new_collection)
        self.assertEqual(self.matrix.last_used_collection, new_collection)

    def test_matrix_set_no_last_used_collection(self):
        self.matrix.set_no_last_used_collection()
        self.assertIsNone(self.matrix.last_used_collection)

    def test_matrix_has_no_last_used_collection(self):
        self.matrix.set_no_last_used_collection()
        self.assertTrue(self.matrix.has_no_last_used_collection())

    def test_matrix_has_last_used_collection(self):
        self.assertTrue(self.matrix.has_last_used_collection())
        self.matrix.set_no_last_used_collection()
        self.assertFalse(self.matrix.has_last_used_collection())

    def test_matrix_set_last_used_tag(self):
        new_tag = Tag.objects.create(name='New Tag')
        self.matrix.set_last_used_tag(new_tag)
        self.assertEqual(self.matrix.last_used_tag, new_tag)

    def test_matrix_set_no_last_used_tag(self):
        self.matrix.set_no_last_used_tag()
        self.assertIsNone(self.matrix.last_used_tag)

    def test_matrix_has_no_last_used_tag(self):
        self.matrix.set_no_last_used_tag()
        self.assertTrue(self.matrix.has_no_last_used_tag())

    def test_matrix_has_last_used_tag(self):
        self.assertTrue(self.matrix.has_last_used_tag())
        self.matrix.set_no_last_used_tag()
        self.assertFalse(self.matrix.has_last_used_tag())

    def test_matrix_is_locked(self):
        self.matrix.set_locked()
        self.assertTrue(self.matrix.is_locked())

    def test_matrix_is_not_locked(self):
        self.matrix.set_unlocked()
        self.assertTrue(self.matrix.is_not_locked())

    def test_matrix_is_public(self):
        self.matrix.set_public()
        self.assertTrue(self.matrix.is_public())

    def test_matrix_is_not_public(self):
        self.matrix.set_private()
        self.assertTrue(self.matrix.is_not_public())

    def test_matrix_is_unlocked(self):
        self.matrix.set_unlocked()
        self.assertTrue(self.matrix.is_unlocked())

    def test_matrix_is_not_unlocked(self):
        self.matrix.set_locked()
        self.assertTrue(self.matrix.is_not_unlocked())

    def test_matrix_is_private(self):
        self.matrix.set_private()
        self.assertTrue(self.matrix.is_private())

    def test_matrix_is_not_private(self):
        self.matrix.set_public()
        self.assertTrue(self.matrix.is_not_private())

    def test_matrix_get_formatted_id(self):
        self.assertEqual(self.matrix.get_formatted_id(), f"CPW:{self.matrix.id:06d}")


if __name__ == '__main__':
    unittest.main()