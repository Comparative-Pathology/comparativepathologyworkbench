from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Credential


class CredentialModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.credential = Credential.objects.create(
            username='testcredential',
            wordpress=1,
            apppwd='password',
            owner=self.user
        )

    def test_credential_creation(self):
        self.assertEqual(self.credential.username, 'testcredential')
        self.assertEqual(self.credential.wordpress, 1)
        self.assertEqual(self.credential.apppwd, 'password')
        self.assertEqual(self.credential.owner, self.user)

    def test_credential_str(self):
        self.assertEqual(str(self.credential), f"{self.credential.id}, testcredential, 1, password, {self.user.id}")

    def test_credential_repr(self):
        self.assertEqual(repr(self.credential), f"{self.credential.id}, testcredential, 1, password, {self.user.id}")

    def test_has_no_apppwd(self):
        self.credential.apppwd = ''
        self.assertTrue(self.credential.has_no_apppwd())
        self.assertFalse(self.credential.has_apppwd())

    def test_has_apppwd(self):
        self.assertTrue(self.credential.has_apppwd())
        self.assertFalse(self.credential.has_no_apppwd())

    def test_is_owned_by(self):
        self.assertTrue(self.credential.is_owned_by(self.user))
        other_user = User.objects.create_user(username='otheruser', password='12345')
        self.assertFalse(self.credential.is_owned_by(other_user))

    def test_set_owner(self):
        new_user = User.objects.create_user(username='newuser', password='12345')
        self.credential.set_owner(new_user)
        self.assertEqual(self.credential.owner, new_user)