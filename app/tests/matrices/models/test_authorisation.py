from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Matrix, Authority, Authorisation


class AuthorisationTestCase(TestCase):

    def setUp(self):
        self.matrix_owner = User.objects.create_user(username='testowner1', password='12345')
        self.authority_owner = User.objects.create_user(username='testowner2', password='12345')
        self.matrix = Matrix.objects.create(title="Test Matrix", owner=self.matrix_owner)
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.authority = Authority.objects.create(name="123456789012", owner=self.authority_owner)
        self.authorisation = Authorisation.objects.create(matrix=self.matrix, permitted=self.user, authority=self.authority)

    def test_authorisation_creation(self):
        self.assertEqual(self.authorisation.matrix, self.matrix)
        self.assertEqual(self.authorisation.permitted, self.user)
        self.assertEqual(self.authorisation.authority, self.authority)

    def test_authorisation_str(self):
        self.assertEqual(str(self.authorisation), f"{self.authorisation.id}, {self.matrix.id}, {self.user.id}, {self.authority.id}")

    def test_authorisation_repr(self):
        self.assertEqual(repr(self.authorisation), f"{self.authorisation.id}, {self.matrix.id}, {self.user.id}, {self.authority.id}")

    def test_is_permitted_by(self):
        self.assertTrue(self.authorisation.is_permitted_by(self.user))
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.assertFalse(self.authorisation.is_permitted_by(another_user))

    def test_is_authority(self):
        self.assertTrue(self.authorisation.is_authority(self.authority))
        another_authority = Authority.objects.create(name="121234567890", owner=self.authority_owner)
        self.assertFalse(self.authorisation.is_authority(another_authority))

    def test_has_authority(self):
        self.assertTrue(self.authorisation.has_authority(self.matrix, self.user))
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.assertFalse(self.authorisation.has_authority(self.matrix, another_user))