from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from matrices.models import Document
from django.utils import timezone


class DocumentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.document = Document.objects.create(
            comment='Test comment',
            source_url='http://example.com',
            location=SimpleUploadedFile(name='testfile.jpg', content=b'', content_type='image/jpeg'),
            owner=self.user
        )

    def test_document_creation(self):
        self.assertEqual(self.document.comment, 'Test comment')
        self.assertEqual(self.document.source_url, 'http://example.com')
        self.assertTrue(self.document.location.name.endswith('testfile.jpg'))
        self.assertEqual(self.document.owner, self.user)

    def test_set_comment(self):
        self.document.set_comment('New comment')
        self.assertEqual(self.document.comment, 'New comment')

    def test_set_source_url(self):
        self.document.set_source_url('http://newexample.com')
        self.assertEqual(self.document.source_url, 'http://newexample.com')

    def test_set_location(self):
        new_file = SimpleUploadedFile(name='newfile.jpg', content=b'', content_type='image/jpeg')
        self.document.set_location(new_file)
        self.assertTrue(self.document.location.name.endswith('newfile.jpg'))

    def test_set_uploaded_at(self):
        new_time = timezone.now()
        self.document.set_uploaded_at(new_time)
        self.assertEqual(self.document.uploaded_at, new_time)

    def test_set_owner(self):
        new_user = User.objects.create_user(username='newuser', password='12345')
        self.document.set_owner(new_user)
        self.assertEqual(self.document.owner, new_user)

    def test_is_owned_by(self):
        self.assertTrue(self.document.is_owned_by(self.user))
        new_user = User.objects.create_user(username='newuser', password='12345')
        self.assertFalse(self.document.is_owned_by(new_user))

    def test_is_duplicate(self):
        duplicate_document = Document(
            comment='Test comment',
            source_url='http://example.com',
            location=self.document.location,
            uploaded_at=self.document.uploaded_at,
            owner=self.user
        )
        self.assertTrue(self.document.is_duplicate(
            duplicate_document.comment,
            duplicate_document.source_url,
            duplicate_document.location,
            duplicate_document.uploaded_at,
            duplicate_document.owner
        ))
        non_duplicate_document = Document(
            comment='Different comment',
            source_url='http://different.com',
            location=self.document.location,
            uploaded_at=self.document.uploaded_at,
            owner=self.user
        )
        self.assertFalse(self.document.is_duplicate(
            non_duplicate_document.comment,
            non_duplicate_document.source_url,
            non_duplicate_document.location,
            non_duplicate_document.uploaded_at,
            non_duplicate_document.owner
        ))