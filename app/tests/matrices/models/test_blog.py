from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Blog, Protocol


class BlogModelTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.protocol = Protocol.objects.create(name='Test Protoco', owner=self.user2)
        self.blog = Blog.objects.create(
            name='Test Blog',
            protocol=self.protocol,
            application='Test Application',
            preamble='Test Preamble',
            postamble='Test Postamble',
            owner=self.user1
        )

    def test_blog_creation(self):
        self.assertEqual(self.blog.name, 'Test Blog')
        self.assertEqual(self.blog.protocol, self.protocol)
        self.assertEqual(self.blog.application, 'Test Application')
        self.assertEqual(self.blog.preamble, 'Test Preamble')
        self.assertEqual(self.blog.postamble, 'Test Postamble')
        self.assertEqual(self.blog.owner, self.user1)

    def test_blog_str(self):
        expected_str = f"{self.blog.id}, {self.blog.name}, {self.blog.protocol.id}, {self.blog.application}, {self.blog.preamble}, {self.blog.postamble}, {self.blog.owner.id}"
        self.assertEqual(str(self.blog), expected_str)

    def test_blog_repr(self):
        expected_repr = f"{self.blog.id}, {self.blog.name}, {self.blog.protocol.id}, {self.blog.application}, {self.blog.preamble}, {self.blog.postamble}, {self.blog.owner.id}"
        self.assertEqual(repr(self.blog), expected_repr)

    def test_is_owned_by(self):
        self.assertTrue(self.blog.is_owned_by(self.user1))
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.assertFalse(self.blog.is_owned_by(another_user))

    def test_set_owner(self):
        another_user = User.objects.create_user(username='anotheruser', password='12345')
        self.blog.set_owner(another_user)
        self.assertEqual(self.blog.owner, another_user)

    def test_get_or_none(self):
        blog = Blog.objects.get_or_none(name='Test Blog')
        self.assertIsNotNone(blog)
        self.assertEqual(blog, self.blog)

        non_existent_blog = Blog.objects.get_or_none(name='Non Existent Blog')
        self.assertIsNone(non_existent_blog)