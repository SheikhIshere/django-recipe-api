"""
Test for modle
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class ModelTest(TestCase):
    def test_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpassword@@'
        user = User.objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    

    def test_new_user_email_normalize(self):
        """test email is normalize for new user"""
        simple_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in simple_email:
            user = User.objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
    
    def test_new_user_without_value_error(self):
        """test that user without raising email vlue error"""
        with self.assertRaises(ValueError):
            User.objects.create_user('', 'test123')
    
    def test_create_super_user(self):
        """test creating superuser"""
        user = User.objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

