"""
Testing api of user
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """create and return new user"""
    return User.objects.create_user(**params)

class PublicUserApiTest(TestCase):
    """test the public features of the user api"""
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        """test creating user is success full"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        self.assertNotIn('password', res.data)
    
    def test_user_with_email_exist_error(self):
        """test error if user's email is already exist in data base"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'test name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_too_short_error(self):
        """giving error if password is too short ew!!"""
        payload = {
            'email': 'test@example.com',
            'password': 'ew',
            'name': 'test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = User.objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exist)

    
    def test_create_token_for_user(self):
        """this is test generate token for valid credintial"""
        user_detail = {
            'name': 'test name',
            'email': 'testemail@example.com',
            'password': 'password123',
        }
        create_user(**user_detail)
        payload = {
            'email': user_detail['email'],
            'password': user_detail['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credential(self):
        """this test return error if credential is invalid"""
        create_user(email = 'testemail@example.com', password = 'password123')

        payload = {'email': 'test@example.com', 'password': 'badpassword'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_blank_password(self):
        """testing if blank password is passed"""
        payload = {'email': 'test234@example.com', 'password':''}
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorize(self):
        """testing authentication is required for user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivetUserTest(TestCase):
    """testing API that require authentication"""
    
    def setUp(self):
        self.user = create_user(
            email = 'test@example.com',
            password = 'password123',
            name = 'test name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user = self.user)

    def test_retrive_profile_success(self):
        """test retriving profile for loggedin user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email' : self.user.email,
        })
    
    def test_post_is_not_allow(self):
        """test post is not allowed for the me endpoint"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_user_profile(self):
        """testing to update user profile"""
        payload = {'name':'update name', 'password': 'newpass123'}

        # res = self.client.patch(ME_URL, {}) # this caused error cz of {}
        res = self.client.patch(ME_URL, payload) # fixed

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        # self.assertEqual(self.user.check_password, payload['password'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
