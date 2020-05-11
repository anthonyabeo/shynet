from django.test import TestCase
from django.db.utils import IntegrityError

from core.models import User


class TestUserModel(TestCase):
    def test_cannot_create_users_with_duplicate_emails(self):
        try:
            user1 = User.objects.create(email="admin@admin.com")
            user2 = User.objects.create(email="admin@admin.com")
        except IntegrityError as e:
            self.assertEquals(str(e), "UNIQUE constraint failed: core_user.email")
            self.assertRaises(IntegrityError)

    def test_creating_users_with_duplicate_username_raises_integrity_error(self):
        try:
            user1 = User.objects.create(
                username="ea6c5a25-41c1-4aeb-8d2d-8a64f86555ff", email="foo@admin.com"
            )
            user2 = User.objects.create(
                username="ea6c5a25-41c1-4aeb-8d2d-8a64f86555ff", email="bar@admin.com"
            )
        except IntegrityError as e:
            self.assertEquals(str(e), "UNIQUE constraint failed: core_user.username")
            self.assertRaises(IntegrityError)

    def test_user_object_is_identified_using_email(self):
        user1 = User.objects.create(email="foo@admin.com")
        user2 = User.objects.create(email="bar@admin.com")
        user3 = User.objects.create(email="baz@admin.com")

        self.assertEquals(user1.__str__(), "foo@admin.com")
        self.assertEquals(user2.__str__(), "bar@admin.com")
        self.assertEquals(user3.__str__(), "baz@admin.com")
