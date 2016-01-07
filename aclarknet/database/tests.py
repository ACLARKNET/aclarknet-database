from django.test import TestCase

# Create your tests here.

from .models import Client
from .utils import edit


class ClientTestCase(TestCase):
    def setUp(self):
        Client.objects.create(name="client-1", active=True)

    def test_client_is_active(self):
        client = Client.objects.get(name="client-1")
        self.assertEqual(client.active, True)


class EditTestCase(TestCase):
    def setUp(self):
        Client.objects.create(name="client-1", active=True)

    def test_edit(self):
        """
        request, form_model, model, url_name, template
        """
        client = Client.objects.get(name="client-1")
