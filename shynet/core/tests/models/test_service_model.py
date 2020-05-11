from django.test import TestCase

from core.models import Service, User


class ServiceModelTest(TestCase):
    def setUp(self):
        super().setUp()
        user1 = User.objects.create(email="admin@admin.com")
        self.service = Service.objects.create(name="service1", owner=user1)

    def test_service_object_identifiable_by_name(self):
        self.assertEquals(self.service.__str__(), "service1")
