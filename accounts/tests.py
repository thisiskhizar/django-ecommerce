from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

CustomUser = get_user_model()

class CustomUserModelTests(TestCase):
    """Tests for the custom user model."""

    def test_create_user(self):
        """Test creating a regular user."""
        user = CustomUser.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            phone_number='+1234567890',
            password='password123'
        )
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.phone_number, '+1234567890')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('password123'))

    def test_create_superuser(self):
        """Test creating a superuser."""
        superuser = CustomUser.objects.create_superuser(
            email='admin@example.com',
            username='adminuser',
            password='adminpass123'
        )
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertEqual(superuser.username, 'adminuser')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_email_is_unique(self):
        """Test that email must be unique."""
        CustomUser.objects.create_user(
            email='unique@example.com',
            username='user1',
            password='password123'
        )
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email='unique@example.com',
                username='user2',
                password='password123'
            )

    def test_username_is_unique(self):
        """Test that username must be unique."""
        CustomUser.objects.create_user(
            email='user1@example.com',
            username='uniqueusername',
            password='password123'
        )
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                email='user2@example.com',
                username='uniqueusername',
                password='password123'
            )

    def test_phone_number_optional(self):
        """Test creating a user without a phone number."""
        user = CustomUser.objects.create_user(
            email='nopho@example.com',
            username='nopho',
            password='password123'
        )
        self.assertIsNone(user.phone_number)

