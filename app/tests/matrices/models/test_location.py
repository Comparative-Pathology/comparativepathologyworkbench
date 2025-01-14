from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Location


class LocationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.location = Location.objects.create(name='Test Location', owner=self.user)

    def test_location_creation(self):
        self.assertEqual(self.location.name, 'Test Location')
        self.assertEqual(self.location.owner, self.user)
        self.assertEqual(self.location.colour, 'FFFFFF')

    def test_location_str(self):
        self.assertEqual(str(self.location), 'Test Location')

    def test_location_repr(self):
        self.assertEqual(repr(self.location), f'Test Location, {self.user.id}')

    def test_location_is_owned_by(self):
        self.assertTrue(self.location.is_owned_by(self.user))
        other_user = User.objects.create_user(username='otheruser', password='12345')
        self.assertFalse(self.location.is_owned_by(other_user))

    def test_location_set_owner(self):
        new_user = User.objects.create_user(username='newuser', password='12345')
        self.location.set_owner(new_user)
        self.assertEqual(self.location.owner, new_user)

    def test_location_get_or_none(self):
        location = Location.objects.get_or_none(name='Test Location')
        self.assertIsNotNone(location)
        self.assertEqual(location.name, 'Test Location')

        location = Location.objects.get_or_none(name='Nonexistent Location')
        self.assertIsNone(location)