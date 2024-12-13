from django.apps import apps
from django.test import TestCase

class PostModelTestCase(TestCase):
    def setUp(self):
        apps.get_app_config('haystack').signal_processor.teardown()
        return super().setUp()