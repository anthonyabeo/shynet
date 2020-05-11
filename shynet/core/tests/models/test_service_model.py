from django.test import TestCase

from core.models import Service, User
from ipaddress import IPv4Network


class ServiceModelTest(TestCase):
    def setUp(self):
        super().setUp()
        user1 = User.objects.create(email="admin@admin.com")
        self.service = Service.objects.create(name="service1", owner=user1)

    def test_service_object_identifiable_by_name(self):
        self.assertEquals(self.service.__str__(), "service1")

    def test_getting_of_ignored_network_list(self):
        ignored_networks = self.service.get_ignored_networks()
        self.assertEquals(len(ignored_networks), 0)

        self.service.ignored_ips = "123.56.78.90, 172.45.6.78/32, 192.168.0.10"
        self.service.save()

        ignored_networks = self.service.get_ignored_networks()

        self.assertIn(IPv4Network("123.56.78.90"), ignored_networks)
        self.assertIn(IPv4Network("172.45.6.78/32"), ignored_networks)
        self.assertIn(IPv4Network("192.168.0.10"), ignored_networks)
