from django.apps import apps
from django.test import TestCase
from matrices.models import ImageSummary, Image
from taggit.models import Tag
from matrices.routines.exists_parent_image_links_for_image import exists_parent_image_links_for_image
from matrices.routines.exists_child_image_links_for_image import exists_child_image_links_for_image


class ImageSummaryTestCase(TestCase):

    def setUp(self):
        self.image = Image.objects.create(id=1, name="Test Image")
        self.tag = Tag.objects.create(name="Test Tag")
        self.collection = apps.get_model('matrices', 'Collection').objects.create(name="Test Collection")
        self.matrix = apps.get_model('matrices', 'Matrix').objects.create(name="Test Matrix")
        self.server = apps.get_model('matrices', 'Server').objects.create(name="Test Server")

        self.image_summary = ImageSummary.objects.create(
            image_id=self.image.id,
            image_tag_ids=str(self.tag.id),
            image_collection_ids=str(self.collection.id),
            image_matrix_ids=str(self.matrix.id),
            image_server_id=self.server.id
        )

    def test_get_or_none(self):
        result = ImageSummary.objects.get_or_none(id=self.image_summary.id)
        self.assertIsNotNone(result)
        result = ImageSummary.objects.get_or_none(id=999)
        self.assertIsNone(result)

    def test_exists_parent_image_links(self):
        exists_parent_image_links_for_image.return_value = True
        self.assertTrue(self.image_summary.exists_parent_image_links())

    def test_exists_child_image_links(self):
        exists_child_image_links_for_image.return_value = True
        self.assertTrue(self.image_summary.exists_child_image_links())

    def test_has_tags(self):
        self.assertTrue(self.image_summary.has_tags())

    def test_get_tags(self):
        tags = self.image_summary.get_tags()
        self.assertIn(self.tag, tags)

    def test_has_this_tag(self):
        self.assertTrue(self.image_summary.has_this_tag(self.tag))

    def test_has_collections(self):
        self.assertTrue(self.image_summary.has_collections())

    def test_get_collections(self):
        collections = self.image_summary.get_collections()
        self.assertIn(self.collection, collections)

    def test_has_this_collection(self):
        self.assertTrue(self.image_summary.has_this_collection(self.collection))

    def test_has_matrices(self):
        self.assertTrue(self.image_summary.has_matrices())

    def test_get_matrices(self):
        matrices = self.image_summary.get_matrices()
        self.assertIn(self.matrix, matrices)

    def test_has_this_matrix(self):
        self.assertTrue(self.image_summary.has_this_matrix(self.matrix))

    def test_get_server(self):
        server = self.image_summary.get_server()
        self.assertEqual(server, self.server)

    def test_is_wordpress(self):
        self.server.is_wordpress.return_value = True
        self.assertTrue(self.image_summary.is_wordpress())

    def test_is_omero547(self):
        self.server.is_omero547.return_value = True
        self.assertTrue(self.image_summary.is_omero547())

    def test_is_ebi_sca(self):
        self.server.is_ebi_sca.return_value = True
        self.assertTrue(self.image_summary.is_ebi_sca())

    def test_is_cpw(self):
        self.server.is_cpw.return_value = True
        self.assertTrue(self.image_summary.is_cpw())