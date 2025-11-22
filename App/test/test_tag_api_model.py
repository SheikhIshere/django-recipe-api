"""this is for testing tag sytem"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import (
    Tag,
    Recipe
)

from django.urls import reverse
from recipe.serializers import TagSerialization

from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()
TAG_URLS = reverse('recipe:tag-list')

def create_user(email = 'test@example.com', password = 'testpass124'):
    """helper function for create and return new user"""
    return User.objects.create_user(email, password)

def detail_url(tag_id):
    """create and return tag detail"""
    return reverse('recipe:tag-detail', args=[tag_id])

class TagTest(TestCase):
    """here i will be testing the tag"""
    def test_creating_tag(self):
        """test of creating tag"""
        user = create_user()
        tag = Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)


class PublicTagApiTest(TestCase):
    """here i will be testing unauthenticated api request"""
    def setUp(self):
        """setting up the tag testing"""
        self.client = APIClient()

    def test_auth_required(self):
        """auth is required while retriving tags"""        
        res = self.client.get(TAG_URLS)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    

class PrivetTagApiTest(TestCase):
    """testing authenticated api request"""
    def setUp(self):
        """setting up"""
        self.user = create_user()
        self.client = APIClient()
        # self.client.force_login(self.user) # use force_authenticate
        self.client.force_authenticate(self.user) # fixed
    
    def test_retriving_tags(self):
        """test: retriving the list of tags"""
        Tag.objects.create(user=self.user, name='meat')
        Tag.objects.create(user=self.user, name='vegan')
        
        res = self.client.get(TAG_URLS)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerialization(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_tags_limited_to_user(self):
        """testing tags which are for limited user like(user's post)"""
        user2 = create_user(email='test2@example.com')
        Tag.objects.filter(user=user2, name='fruti')
        tag = Tag.objects.create(user=self.user, name='good-food')

        res = self.client.get(TAG_URLS)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)
    
    def test_update_tag(self):
        """Test: updatinng tags here"""
        tag = Tag.objects.create(user = self.user, name = 'after dinner')

        payload = {'name': 'desart'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])
    
    def test_delete_tag(self):
        """deleting a tag"""
        tag = Tag.objects.create(user=self.user, name='break_fast')

        # url = detail_url(TAG_URLS) # i should use tag.id cz it want that
        url = detail_url(tag.id) # fixed
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

    def test_filter_tags_assigned_to_recipes(self):
        """Test listing tags to those assigned to recipes."""
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        recipe = Recipe.objects.create(
            title='Green Eggs on Toast',
            time_minutes=10,
            price=Decimal('2.50'),
            user=self.user,
        )
        recipe.tags.add(tag1)

        res = self.client.get(TAG_URLS, {'assigned_only': 1})

        s1 = TagSerialization(tag1)
        s2 = TagSerialization(tag2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_tags_unique(self):
        """Test filtered tags returns a unique list."""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Dinner')
        recipe1 = Recipe.objects.create(
            title='Pancakes',
            time_minutes=5,
            price=Decimal('5.00'),
            user=self.user,
        )
        recipe2 = Recipe.objects.create(
            title='Porridge',
            time_minutes=3,
            price=Decimal('2.00'),
            user=self.user,
        )
        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        res = self.client.get(TAG_URLS, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
