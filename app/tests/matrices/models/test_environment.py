from django.test import TestCase
from django.contrib.auth.models import User
from matrices.models import Environment
from matrices.models.location import Location
from matrices.models.protocol import Protocol
from matrices.models.gateway import Gateway


class EnvironmentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.location = Location.objects.create(name='Test Location')
        self.protocol = Protocol.objects.create(name='http')
        self.gateway = Gateway.objects.create(name='WEB')

        self.environment = Environment.objects.create(
            name='Test Environment',
            location=self.location,
            protocol=self.protocol,
            web_root='www.test.com',
            document_root='/var/www/test',
            nginx_private_location='/private',
            wordpress_web_root='www.wordpress.com',
            from_email='test@test.com',
            date_format='%A, %B %e, %Y',
            owner=self.user,
            minimum_cell_height=75,
            maximum_cell_height=450,
            minimum_cell_width=75,
            maximum_cell_width=450,
            maximum_initial_columns=10,
            minimum_initial_columns=1,
            maximum_initial_rows=10,
            minimum_initial_rows=1,
            maximum_rest_columns=1000,
            minimum_rest_columns=3,
            maximum_rest_rows=1000,
            minimum_rest_rows=3,
            maximum_bench_count=10,
            maximum_collection_count=10,
            gateway=self.gateway,
            gateway_port=80,
            gateway_pagination=50,
            background_processing=False,
            window_refresh_time=10,
            task_pause_time=5
        )

    def test_environment_creation(self):
        self.assertEqual(self.environment.name, 'Test Environment')
        self.assertEqual(self.environment.location, self.location)
        self.assertEqual(self.environment.protocol, self.protocol)
        self.assertEqual(self.environment.web_root, 'www.test.com')
        self.assertEqual(self.environment.document_root, '/var/www/test')
        self.assertEqual(self.environment.nginx_private_location, '/private')
        self.assertEqual(self.environment.wordpress_web_root, 'www.wordpress.com')
        self.assertEqual(self.environment.from_email, 'test@test.com')
        self.assertEqual(self.environment.date_format, '%A, %B %e, %Y')
        self.assertEqual(self.environment.owner, self.user)
        self.assertEqual(self.environment.minimum_cell_height, 75)
        self.assertEqual(self.environment.maximum_cell_height, 450)
        self.assertEqual(self.environment.minimum_cell_width, 75)
        self.assertEqual(self.environment.maximum_cell_width, 450)
        self.assertEqual(self.environment.maximum_initial_columns, 10)
        self.assertEqual(self.environment.minimum_initial_columns, 1)
        self.assertEqual(self.environment.maximum_initial_rows, 10)
        self.assertEqual(self.environment.minimum_initial_rows, 1)
        self.assertEqual(self.environment.maximum_rest_columns, 1000)
        self.assertEqual(self.environment.minimum_rest_columns, 3)
        self.assertEqual(self.environment.maximum_rest_rows, 1000)
        self.assertEqual(self.environment.minimum_rest_rows, 3)
        self.assertEqual(self.environment.maximum_bench_count, 10)
        self.assertEqual(self.environment.maximum_collection_count, 10)
        self.assertEqual(self.environment.gateway, self.gateway)
        self.assertEqual(self.environment.gateway_port, 80)
        self.assertEqual(self.environment.gateway_pagination, 50)
        self.assertEqual(self.environment.background_processing, False)
        self.assertEqual(self.environment.window_refresh_time, 10)
        self.assertEqual(self.environment.task_pause_time, 5)

    def test_get_window_refresh_time_milliseconds(self):
        self.assertEqual(self.environment.get_window_refresh_time_milliseconds(), 10000)

    def test_get_task_pause_time_milliseconds(self):
        self.assertEqual(self.environment.get_task_pause_time_milliseconds(), 5000)

    def test_get_full_web_root(self):
        self.assertEqual(self.environment.get_full_web_root(), 'http://www.test.com')

    def test_is_owned_by(self):
        self.assertTrue(self.environment.is_owned_by(self.user))
        another_user = User.objects.create(username='anotheruser')
        self.assertFalse(self.environment.is_owned_by(another_user))

    def test_is_cpw(self):
        self.environment.name = 'CPW'
        self.assertTrue(self.environment.is_cpw())
        self.environment.name = 'Not CPW'
        self.assertFalse(self.environment.is_cpw())

    def test_is_czi(self):
        self.location.name = 'CZI'
        self.assertTrue(self.environment.is_czi())
        self.location.name = 'Not CZI'
        self.assertFalse(self.environment.is_czi())

    def test_is_canada(self):
        self.location.name = 'CANADA'
        self.assertTrue(self.environment.is_canada())
        self.location.name = 'Not CANADA'
        self.assertFalse(self.environment.is_canada())

    def test_is_coeliac(self):
        self.location.name = 'COELIAC'
        self.assertTrue(self.environment.is_coeliac())
        self.location.name = 'Not COELIAC'
        self.assertFalse(self.environment.is_coeliac())

    def test_is_development(self):
        self.location.name = 'DEVELOPMENT'
        self.assertTrue(self.environment.is_development())
        self.location.name = 'Not DEVELOPMENT'
        self.assertFalse(self.environment.is_development())

    def test_is_blitz_gateway(self):
        self.gateway.name = 'BLITZ'
        self.assertTrue(self.environment.is_blitz_gateway())
        self.gateway.name = 'Not BLITZ'
        self.assertFalse(self.environment.is_blitz_gateway())

    def test_is_web_gateway(self):
        self.gateway.name = 'WEB'
        self.assertTrue(self.environment.is_web_gateway())
        self.gateway.name = 'Not WEB'
        self.assertFalse(self.environment.is_web_gateway())

    def test_is_wordpress_active(self):
        self.environment.wordpress_active = True
        self.assertTrue(self.environment.is_wordpress_active())
        self.environment.wordpress_active = False
        self.assertFalse(self.environment.is_wordpress_active())

    def test_is_background_processing(self):
        self.environment.background_processing = True
        self.assertTrue(self.environment.is_background_processing())
        self.environment.background_processing = False
        self.assertFalse(self.environment.is_background_processing())

    def test_is_foreground_processing(self):
        self.environment.background_processing = False
        self.assertTrue(self.environment.is_foreground_processing())
        self.environment.background_processing = True
        self.assertFalse(self.environment.is_foreground_processing())