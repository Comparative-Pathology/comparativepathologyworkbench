from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Protocol


class ProtocolTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.protocol = Protocol.objects.create(name='TestProtocol', owner=self.user)

    def test_protocol_creation(self):
        self.assertEqual(self.protocol.name, 'TestProtocol')
        self.assertEqual(self.protocol.owner, self.user)

    def test_protocol_str(self):
        self.assertEqual(str(self.protocol), 'TestProtocol')

    def test_protocol_repr(self):
        self.assertEqual(repr(self.protocol), f'TestProtocol, {self.user.id}')

    def test_protocol_is_owned_by(self):
        self.assertTrue(self.protocol.is_owned_by(self.user))
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.assertFalse(self.protocol.is_owned_by(another_user))

    def test_protocol_set_owner(self):
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.protocol.set_owner(another_user)
        self.assertEqual(self.protocol.owner, another_user)

    def test_protocol_get_or_none(self):
        protocol = Protocol.objects.get_or_none(name='TestProtocol')
        self.assertIsNotNone(protocol)
        self.assertEqual(protocol.name, 'TestProtocol')

        non_existent_protocol = Protocol.objects.get_or_none(name='NonExistent')
        self.assertIsNone(non_existent_protocol)