"""test model ingredient"""

from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from django.test import TestCase
from recipe.models import (
    Recipe,
    Ingredient,

)
from recipe.serializers import (
    IngredientSerializer,
)

from django.contrib.auth import get_user_model

User = get_user_model()
INGREDIENT_URLS = reverse('recipe:ingredient-list')

def create_user(email = 'test@example.com', password = 'testpass124'):
    """helper function for create and return new user"""
    return User.objects.create_user(email, password)

def detail_url(ingredient_id):
    """create and return tag detail"""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_ingredient(user, name='banana'):
    return Ingredient.objects.create(user=user, name=name)



class FirstIngredientTest(TestCase):
    """here i am starting testing ingredient"""

    def test_create_ingredient(self):
        """Test creating ingredient success full"""
        user = create_user()
        ingredient = create_ingredient(user=user)

        self.assertEqual(str(ingredient), ingredient.name)


class PublicIngredientApiTest(TestCase):
    """here i am testing the api if unauthenticated user try to retrive"""
    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """Test auth require for retriving ingredient"""
        res = self.client.get(INGREDIENT_URLS)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivetApiTest(TestCase):
    """Test unauthenticated api request"""
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrive_ingredient(self):
        """Test: an authenticated user trying to retrive the data """
        create_ingredient(user=self.user, name='banana')
        create_ingredient(user=self.user, name='penut')

        res = self.client.get(INGREDIENT_URLS)

        ingredient = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredient, many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """ingredient authenticated to user"""
        user2 = create_user(email='newtest@example.com')
        create_ingredient(user=user2)
        ingredient = create_ingredient(user=self.user, name='pepper')
        
        res = self.client.get(INGREDIENT_URLS)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)
    
    def test_update_ingredient(self):
        """Test updating an ingredient"""
        ingredient = create_ingredient(user=self.user)
        
        payload = {'name': 'pepper'}
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        
        self.assertEqual(ingredient.name, payload['name'])
    
    def test_delete_ingredient(self):
        """test: deleting an ingredient"""
        ingredient = create_ingredient(user=self.user)

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        ingredient = Ingredient.objects.filter(user=self.user)

        self.assertFalse(ingredient.exists())

    def test_filter_ingredients_assigned_to_recipes(self):
       """Test listing ingredients to those assigned to recipes."""
       in1 = Ingredient.objects.create(user=self.user, name='Apples')
       in2 = Ingredient.objects.create(user=self.user, name='Turkey')
       recipe = Recipe.objects.create(
           title='Apple Crumble',
           time_minutes=5,
           price=Decimal('4.50'),
           user=self.user,
       )
       recipe.ingredient.add(in1)
       res = self.client.get(INGREDIENT_URLS, {'assigned_only': 1})
       s1 = IngredientSerializer(in1)
       s2 = IngredientSerializer(in2)
       self.assertIn(s1.data, res.data)
       self.assertNotIn(s2.data, res.data)


    def test_filtered_ingredients_unique(self):
        """Test filtered ingredients returns a unique list."""
        ing = Ingredient.objects.create(user=self.user, name='Eggs')
        Ingredient.objects.create(user=self.user, name='Lentils')
        recipe1 = Recipe.objects.create(
            title='Eggs Benedict',
            time_minutes=60,
            price=Decimal('7.00'),
            user=self.user,
        )
        recipe2 = Recipe.objects.create(
            title='Herb Eggs',
            time_minutes=20,
            price=Decimal('4.00'),
            user=self.user,
        )
        recipe1.ingredient.add(ing)
        recipe2.ingredient.add(ing)

        res = self.client.get(INGREDIENT_URLS, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)