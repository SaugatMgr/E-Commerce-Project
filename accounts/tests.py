from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email = "test_user1@gmail.com",
            password = "test_pwd123",
        )
        self.assertEqual(user.email, "test_user1@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
        try:
            # This should return True because there is no username option for AbstractUser
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="test_pwd123")
            
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email = "admin_user1@gmail.com",
            password = "test_pwd123",
        )
        self.assertEqual(admin_user.email, "admin_user1@gmail.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        
        try:
            # This should return True because there is no username option for AbstractUser
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="admin_user1@gmail.com",
                                     password="test_pwd123",
                                     is_superuser=False)
