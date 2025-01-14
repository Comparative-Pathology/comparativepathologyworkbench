from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models.artefact import Artefact
from datetime import datetime


class ArtefactTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.artefact1 = Artefact.objects.create(
            comment='Test comment',
            location='test_location.zip',
            url='http://example.com',
            uploaded_at=datetime.now(),
            owner=self.user1
        )

    def test_is_duplicate_true(self):
        duplicate_artefact = Artefact(
            comment='Test comment',
            location='test_location.zip',
            url='http://example.com',
            uploaded_at=self.artefact1.uploaded_at,
            owner=self.user1
        )
        self.assertTrue(self.artefact1.is_duplicate(
            duplicate_artefact.comment,
            duplicate_artefact.location,
            duplicate_artefact.uploaded_at,
            duplicate_artefact.owner
        ))

    def test_is_duplicate_false_different_comment(self):
        duplicate_artefact = Artefact(
            comment='Different comment',
            location='test_location.zip',
            url='http://example.com',
            uploaded_at=self.artefact1.uploaded_at,
            owner=self.user1
        )
        self.assertFalse(self.artefact1.is_duplicate(
            duplicate_artefact.comment,
            duplicate_artefact.location,
            duplicate_artefact.uploaded_at,
            duplicate_artefact.owner
        ))

    def test_is_duplicate_false_different_location(self):
        duplicate_artefact = Artefact(
            comment='Test comment',
            location='different_location.zip',
            url='http://example.com',
            uploaded_at=self.artefact1.uploaded_at,
            owner=self.user1
        )
        self.assertFalse(self.artefact1.is_duplicate(
            duplicate_artefact.comment,
            duplicate_artefact.location,
            duplicate_artefact.uploaded_at,
            duplicate_artefact.owner
        ))

    def test_is_duplicate_false_different_uploaded_at(self):
        duplicate_artefact = Artefact(
            comment='Test comment',
            location='test_location.zip',
            url='http://example.com',
            uploaded_at=datetime.now(),
            owner=self.user1
        )
        self.assertFalse(self.artefact1.is_duplicate(
            duplicate_artefact.comment,
            duplicate_artefact.location,
            duplicate_artefact.uploaded_at,
            duplicate_artefact.owner
        ))

    def test_is_duplicate_false_different_owner(self):
        duplicate_artefact = Artefact(
            comment='Test comment',
            location='test_location.zip',
            url='http://example.com',
            uploaded_at=self.artefact1.uploaded_at,
            owner=self.user2
        )
        self.assertFalse(self.artefact1.is_duplicate(
            duplicate_artefact.comment,
            duplicate_artefact.location,
            duplicate_artefact.uploaded_at,
            duplicate_artefact.owner
        ))