from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Command, Protocol, Type


class CommandModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.protocol = Protocol.objects.create(name='Test Protocol')
        self.type = Type.objects.create(name='Test Type')
        self.command = Command.objects.create(
            name='Test Command',
            application='Test Application',
            preamble='Test Preamble',
            postamble='Test Postamble',
            protocol=self.protocol,
            type=self.type,
            owner=self.user
        )

    def test_command_creation(self):
        self.assertEqual(self.command.name, 'Test Command')
        self.assertEqual(self.command.application, 'Test Application')
        self.assertEqual(self.command.preamble, 'Test Preamble')
        self.assertEqual(self.command.postamble, 'Test Postamble')
        self.assertEqual(self.command.protocol, self.protocol)
        self.assertEqual(self.command.type, self.type)
        self.assertEqual(self.command.owner, self.user)

    def test_command_str(self):
        expected_str = f"{self.command.id}, {self.command.name}, {self.command.application}, {self.command.preamble}, {self.command.postamble}, {self.command.protocol.id}, {self.command.type.id}, {self.command.owner.id}"
        self.assertEqual(str(self.command), expected_str)

    def test_command_repr(self):
        expected_repr = f"{self.command.id}, {self.command.name}, {self.command.application}, {self.command.preamble}, {self.command.postamble}, {self.command.protocol.id}, {self.command.type.id}, {self.command.owner.id}"
        self.assertEqual(repr(self.command), expected_repr)

    def test_is_owned_by(self):
        self.assertTrue(self.command.is_owned_by(self.user))
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.assertFalse(self.command.is_owned_by(another_user))

    def test_set_owner(self):
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.command.set_owner(another_user)
        self.assertEqual(self.command.owner, another_user)