from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Profile, Collection


class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.collection1 = Collection.objects.create(name='Collection 1')
        self.collection2 = Collection.objects.create(name='Collection 2')
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio',
            location='Test location',
            birth_date='2000-01-01',
            email_confirmed=True,
            active_collection=self.collection1,
            last_used_collection=self.collection2,
            hide_collection_image=True
        )

    def test_profile_creation(self):
        self.assertIsInstance(self.profile, Profile)
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.bio, 'Test bio')
        self.assertEqual(self.profile.location, 'Test location')
        self.assertEqual(self.profile.birth_date, '2000-01-01')
        self.assertTrue(self.profile.email_confirmed)
        self.assertEqual(self.profile.active_collection, self.collection1)
        self.assertEqual(self.profile.last_used_collection, self.collection2)
        self.assertTrue(self.profile.hide_collection_image)

    def test_profile_str(self):
        self.assertEqual(str(self.profile), f"{self.profile.id}, Test bio, Test location, 2000-01-01, True, {self.collection1}, {self.collection2}, True")

    def test_profile_repr(self):
        self.assertEqual(repr(self.profile), f"{self.profile.id}, {self.user.id}, Test bio, Test location, 2000-01-01, True, {self.collection1}, {self.collection2}, True")

    def test_set_active_collection(self):
        new_collection = Collection.objects.create(name='New Collection')
        self.profile.set_active_collection(new_collection)
        self.assertEqual(self.profile.active_collection, new_collection)

    def test_set_last_used_collection(self):
        new_collection = Collection.objects.create(name='New Collection')
        self.profile.set_last_used_collection(new_collection)
        self.assertEqual(self.profile.last_used_collection, new_collection)

    def test_set_hide_collection_image(self):
        self.profile.set_hide_collection_image(False)
        self.assertFalse(self.profile.hide_collection_image)

    def test_has_active_collection(self):
        self.assertTrue(self.profile.has_active_collection())
        self.profile.active_collection = None
        self.assertFalse(self.profile.has_active_collection())

    def test_has_last_used_collection(self):
        self.assertTrue(self.profile.has_last_used_collection())
        self.profile.last_used_collection = None
        self.assertFalse(self.profile.has_last_used_collection())

    def test_is_hide_collection_image(self):
        self.assertTrue(self.profile.is_hide_collection_image())
        self.profile.hide_collection_image = False
        self.assertFalse(self.profile.is_hide_collection_image())

    def test_post_save_signal(self):
        new_user = User.objects.create_user(username='newuser', password='12345')
        self.assertIsInstance(new_user.profile, Profile)