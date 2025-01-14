from django.test import TestCase
from matrices.models import Image, Artefact, ImageLink


class ImageLinkTestCase(TestCase):
    def setUp(self):
        self.parent_image = Image.objects.create(name="Parent Image")
        self.child_image = Image.objects.create(name="Child Image")
        self.artefact = Artefact.objects.create(name="Artefact")
        self.image_link = ImageLink.objects.create(
            parent_image=self.parent_image,
            child_image=self.child_image,
            artefact=self.artefact
        )

    def test_create_image_link(self):
        self.assertEqual(self.image_link.parent_image, self.parent_image)
        self.assertEqual(self.image_link.child_image, self.child_image)
        self.assertEqual(self.image_link.artefact, self.artefact)

    def test_set_parent_image(self):
        new_parent_image = Image.objects.create(name="New Parent Image")
        self.image_link.set_parent_image(new_parent_image)
        self.assertEqual(self.image_link.parent_image, new_parent_image)

    def test_set_child_image(self):
        new_child_image = Image.objects.create(name="New Child Image")
        self.image_link.set_child_image(new_child_image)
        self.assertEqual(self.image_link.child_image, new_child_image)

    def test_set_artefact(self):
        new_artefact = Artefact.objects.create(name="New Artefact")
        self.image_link.set_artefact(new_artefact)
        self.assertEqual(self.image_link.artefact, new_artefact)

    def test_is_duplicate(self):
        duplicate = self.image_link.is_duplicate(self.parent_image, self.child_image, self.artefact)
        self.assertTrue(duplicate)

        non_duplicate = self.image_link.is_duplicate(self.parent_image, self.child_image, Artefact.objects.create(name="Different Artefact"))
        self.assertFalse(non_duplicate)

    def test_get_owner(self):
        owner = self.image_link.get_owner()
        self.assertEqual(owner, self.artefact.owner)

    def test_is_owned_by(self):
        user = self.artefact.owner
        self.assertTrue(self.image_link.is_owned_by(user))

        another_user = User.objects.create(username="another_user")
        self.assertFalse(self.image_link.is_owned_by(another_user))