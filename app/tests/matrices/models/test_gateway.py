from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Gateway


class GatewayModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.gateway = Gateway.objects.create(name='Test Gateway', owner=self.user)

    def test_gateway_creation(self):
        self.assertEqual(self.gateway.name, 'Test Gateway')
        self.assertEqual(self.gateway.owner, self.user)

    def test_gateway_str(self):
        self.assertEqual(str(self.gateway), 'Test Gateway')

    def test_gateway_repr(self):
        self.assertEqual(repr(self.gateway), f'Test Gateway, {self.user.id}')

    def test_is_owned_by(self):
        self.assertTrue(self.gateway.is_owned_by(self.user))
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.assertFalse(self.gateway.is_owned_by(another_user))

    def test_set_owner(self):
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.gateway.set_owner(another_user)
        self.assertEqual(self.gateway.owner, another_user)

    def test_get_or_none(self):
        gateway = Gateway.objects.get_or_none(name='Test Gateway')
        self.assertIsNotNone(gateway)
        self.assertEqual(gateway, self.gateway)

        non_existent_gateway = Gateway.objects.get_or_none(name='Non Existent Gateway')
        self.assertIsNone(non_existent_gateway)