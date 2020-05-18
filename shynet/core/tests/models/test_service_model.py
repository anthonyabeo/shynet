from django.test import TestCase

from core.models import Service, User
from ipaddress import IPv4Network

from re import Pattern


class ServiceModelTest(TestCase):
    fixtures = [
        "core/fixtures/user.json",
        "core/fixtures/service.json",
        "analytics/fixtures/session.json",
        "analytics/fixtures/hit.json",
    ]

    def setUp(self):
        super().setUp()
        self.service = Service.objects.all()[0]

    def test_service_object_identifiable_by_name(self):
        self.assertEquals(self.service.__str__(), "Demo")

    def test_getting_of_ignored_network_list(self):
        ignored_networks = self.service.get_ignored_networks()
        self.assertEquals(len(ignored_networks), 0)

        self.service.ignored_ips = "123.56.78.90, 172.45.6.78/32, 192.168.0.10"
        self.service.save()

        ignored_networks = self.service.get_ignored_networks()

        self.assertIn(IPv4Network("123.56.78.90"), ignored_networks)
        self.assertIn(IPv4Network("172.45.6.78/32"), ignored_networks)
        self.assertIn(IPv4Network("192.168.0.10"), ignored_networks)

    def test_get_core_data(self):
        core_data = self.service.get_core_stats()

        self.assertAlmostEquals(core_data["avg_hits_per_session"], 1.3333333333333333)
        self.assertAlmostEquals(core_data["avg_load_time"], 55477.25)
        self.assertAlmostEquals(core_data["avg_session_duration"], 637.751)
        self.assertAlmostEquals(core_data["bounce_rate_pct"], 66.66666666666667)

        for browser in core_data["browsers"].all():
            self.assertIn(browser["browser"], ["Firefox", "Chrome"])

        for device_type in core_data["device_types"].all():
            self.assertIn(
                device_type["device_type"],
                ["DESKTOP", "PHONE", "TABLET", "DESKTOP", "ROBOT", "OTHER"],
            )

        for device in core_data["devices"].all():
            self.assertEquals(device["device"], "Mac")
