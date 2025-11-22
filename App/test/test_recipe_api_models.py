"""test for the models like recipe + etc"""

from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO


import tempfile
import os
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from django.test import TestCase
from recipe.models import (
    Recipe,
    Tag,
    Ingredient,
    recipe_image_file_path,
)
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailsSerializer,    
)
from PIL import Image
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

RECIPE_URLS = reverse('recipe:recipe-list')


def image_uploade_url(recipe_id):
    """create and return an image upload url"""
    return reverse('recipe:recipe-upload-image', args=[recipe_id]) 


def create_recipe(user, **params):
    """create and return simple recipe"""
    default = {
        'title': 'simple recipe',
        'description': 'example discription',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'link': 'http://example.com//recipe.pdf'
    }

    default.update(params)
    recipe = Recipe.objects.create(user = user, **default)
    return recipe

def details_urls(recipe_id):
    """creating and returninng recipe urls"""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_user(**params):
    """create_and_return_new_user"""
    return User.objects.create_user(
        **params
    )


class RecipeTesting(TestCase):
    """testing recipe"""

    def test_create_recipe(self):
        """testing creating recipe is successfull"""
        user = User.objects.create_user(
            'test@example.com',
            'testpass123',
        )
        recipe = Recipe.objects.create(
            user = user,
            title = 'example recipe name',
            description = 'Sample of recipe',
            time_minutes = 5,
            price = Decimal('5.50'),
            link = 'none',
        )

        self.assertEqual(str(recipe), recipe.title)


class PublicRecipeApiTest(TestCase):
    """testing for the unauthenticated api request"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_require(self):
        """Test: auth is require to call api"""
        res = self.client.get(RECIPE_URLS)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivetRecipeApiTest(TestCase):
    """Tast: authenticate recipe api call"""

    def setUp(self):
        self.client = APIClient()

        # i am removing this cz i have created helper function to do that
        # self.user = User.objects.create_user(
        #     'test@example.com',            
        #     'testpass123',
        # )

        # helper function related user creation
        self.user = create_user(email='test2@example.com', password='testpass123')
        self.client.force_authenticate(self.user)
    
    def test_retrive_recipe(self):
        """Test: retriving list of recipe"""
        create_recipe(user= self.user)
        create_recipe(user= self.user)

        res = self.client.get(RECIPE_URLS)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_recipe_list_limited_to_user(self):
        """Test list of recipe is limited to authenticated user"""
        # removing this cz i am using helper function
        # other_user = User.objects.create_user(
        #     'otheruser@example.com',
        #     'otheruserpass123'
        # )
        other_user = create_user(email='otheruser@example.com', password='otheruserpass123')
        create_recipe(user = other_user)
        create_recipe(user = self.user)

        res = self.client.get(RECIPE_URLS)

        recipes = Recipe.objects.filter(user = self.user)
        serializer = RecipeSerializer(recipes, many = True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """test get recipe detail"""
        recipe = create_recipe(user = self.user)

        url = details_urls(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailsSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """test creating recipe"""
        payload = {
            'title': 'Cat comb meat dish',
            'description': 'delicious cat food, yum!!',
            'time_minutes': 30,
            'price': Decimal('3.99'),
            'link': 'https://www.youtube.com/shorts/dko1j1V0HsI',
        }
        res = self.client.post(RECIPE_URLS, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])

        for k,v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        
        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Test partial update for recipe"""
        original_link = 'https://example.com/recipe.pdf'
        recipe = create_recipe(
            user=self.user,
            title = 'test title',
            link = original_link,
        )
        payload = {'title':'new recipe title'}
        url = details_urls(recipe_id=recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)
    
    def test_full_update(self):
        """test full update of recipe"""
        recipe = create_recipe(
            user=self.user,
            title = 'new recipe title',
            description = 'new recipe description',
            link = 'https://example.com/recipe.pdf',
        )
        payload = {
            'title': 'Cat comb meat dish',
            'description': 'delicious cat food, yum!!',
            'time_minutes': 30,
            'price': Decimal('3.99'),
            'link': 'https://www.youtube.com/shorts/dko1j1V0HsI',
        }

        url = details_urls(recipe_id=recipe.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()

        for k,v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)
    
    def test_update_user_return_error(self):
        """test changing the recipe user results in the error"""
        # new_user =  create_user(email='test2@example.com', password='testpass123')
        new_user = create_user(email='otheruser@example.com', password='testpass123')
        recipe = create_recipe(user=self.user)
        payload = {'user':new_user.id}
        url = details_urls(recipe_id=recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)
    
    def test_delete_recipe(self):
        """test deleteing a recipe successfully"""
        recipe = create_recipe(user=self.user)

        url = details_urls(recipe_id=recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())
    
    def test_recipe_other_users_recipe_error(self):
        """test: trying to delet other user's recipe"""
        new_user = create_user(
            email = 'new3@example.com',
            password = 'password123'
        )
        recipe = create_recipe(user=new_user)

        url = details_urls(recipe_id=recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())

    def test_create_recipe_with_new_tags(self):
        """ test: creating recipe with new tags """
        payload = {
            'title': 'thai prawn curry',
            'time_minutes': 30,
            'price': Decimal('30.99'),
            # finally found the problemm; this have a syntex error
            # 'tags': {
            #     'name': 'thai',
            #     'name': 'dinner',
            # }
            'tags': [
                {'name': 'thai'},
                {'name': 'dinner'},
            ]
        }

        res = self.client.post(RECIPE_URLS, payload, format='json')

        # so this is causing the getting failled , referaring = 400(bad request)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        
        
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)

        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name = tag['name'],
                user = self.user,
            ).exists()
            self.assertTrue(exists)
    
    def test_create_recipe_with_existing_tag(self):
        """Test: creating same tag to raise error if exists"""
        tag_indian = Tag.objects.create(user=self.user, name='indian')
        payload = {
            'title': 'dosa',
            'time_minutes':20,
            'price': Decimal('1.50'),
            'tags':[
                {'name': 'indian'},
                {'name': 'south-indian'},
                {'name': 'breakfast'},
            ]
        }

        res = self.client.post(RECIPE_URLS, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 3)
        self.assertIn(tag_indian, recipe.tags.all())

        for tag in payload['tags']:
            exists = recipe.tags.filter(
                name = tag['name'],
                user = self.user
            ).exists()
            self.assertTrue(exists)
    
    def test_create_tags_on_update(self):
        """Test: creating tags when updating recipe"""
        recipe = create_recipe(user=self.user)
        payload = {
            'tags': [
                {'name': 'lunch'}
            ]
        }
        url = details_urls(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        new_tag = Tag.objects.get(user=self.user, name='lunch')
        self.assertIn(new_tag, recipe.tags.all())
    
    def test_update_assign_tag(self):
        """test: assigning a tags existing tags while updating"""
        tag_breakfast = Tag.objects.create(user=self.user, name='breakfast')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag_breakfast)

        tag_lunch = Tag.objects.create(user=self.user, name='lunch')
        payload = {'tags': [{'name': 'lunch'}]}
        url = details_urls(recipe_id=recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_lunch, recipe.tags.all())
        self.assertNotIn(tag_breakfast, recipe.tags.all())
    
    def test_clear_recipe_tags(self):
        """Test: clearing recipe's tags"""
        tag = Tag.objects.create(user=self.user, name='Dessart')
        recipe = create_recipe(user=self.user)
        recipe.tags.add(tag)
        payload = {
            'tags':[]
        }
        url = details_urls(recipe_id=recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)
    
    # def test_create_recipe_with_new_ingredient(self):
    #     """here i am testing recipe with new  ingreadient"""

    #     payload = {
    #         'name': 'burger',
    #         'time_minutes': 30,
    #         'price': Decimal('3.99'),
    #         'ingredients': [{'name': 'potato', 'name': 'pepper'}]
    #     }

    #     res = self.client.post(RECIPE_URLS, payload, format='json')

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     recipes = Recipe.objects.filter(user=self.user)
    #     self.assertEqual(recipes.count(), 1)
    #     recipe = recipes[0]
    #     self.assertEqual(recipe.ingredient.count(), 2)

    #     for ingredient in payload['ingredient']:
    #         exists = recipe.objects.filter(
    #             user=self.user, 
    #             name=ingredient['name']
    #         ).exists()
    #         self.assertTrue(exists)
    
    # def test_create_recipe_with_existing_ingredient(self):
    #     """Test: creating recipe with existing ingreating"""
    #     ingredient = Ingredient.objects.create(user=self.user, name='lemon')
    #     payload = {
    #         'title': 'chiness soup',
    #         'time_minutes': 30,
    #         'price': Decimal('9.33'),
    #         'ingredients': [{'name': 'lemon', 'name': 'dog'}],
    #     }

    #     res = self.client.post(RECIPE_URLS, payload, format='json')

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     recipes = Recipe.objects.filter(user=self.user)
    #     self.assertEqual(recipes.count(), 1)
    #     recipe = recipes[0]
    #     self.assertEqual(recipe.ingredient.count(), 2)
    #     self.assertIn(ingredient, recipe.ingredient.all())
    #     for ingredient in payload['ingredient']:
    #         exists = recipe.objects.filter(
    #             name = ingredient['name'],
    #             user = self.user
    #         ).exists()
    #         self.assertTrue(exists)

    # newly implemented in order to fix the bug
    def test_create_recipe_with_new_ingredient(self):
        payload = {
            'title': 'burger',
            'time_minutes': 30,
            'price': Decimal('3.99'),
            'ingredient': [{'name': 'potato'}, {'name': 'pepper'}]
        }
        res = self.client.post(RECIPE_URLS, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(user=self.user)
        self.assertEqual(recipe.ingredient.count(), 2)
        for i in payload['ingredient']:
            self.assertTrue(recipe.ingredient.filter(name=i['name'], user=self.user).exists())

    def test_create_recipe_with_existing_ingredient(self):
        ing = Ingredient.objects.create(user=self.user, name='lemon')
        payload = {
            'title': 'chiness soup',
            'time_minutes': 30,
            'price': Decimal('9.33'),
            'ingredient': [{'name': 'lemon'}, {'name': 'dog'}]
        }
        res = self.client.post(RECIPE_URLS, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(user=self.user)
        self.assertEqual(recipe.ingredient.count(), 2)
        self.assertIn(ing, recipe.ingredient.all())

    def test_ingredient_on_update(self):
        """Test: creating ingredient while updating a recipe"""
        recipe = create_recipe(self.user)

        payload = {'ingredient': [{'name': 'limes'}]}
        url = details_urls(recipe_id=recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        new_ingredient = Ingredient.objects.get(user=self.user, name='limes')
        self.assertIn(new_ingredient, recipe.ingredient.all())
    
    def test_update_recipe_assign_ingredient(self):
        """Test assigning an existing ingredient while updating a recipe"""
        ingredient1 = Ingredient.objects.create(user=self.user, name='pepper')
        recipe = create_recipe(user=self.user)
        recipe.ingredient.add(ingredient1)
        
        ingredient2 = Ingredient.objects.create(user=self.user, name='chili')
        payload = {'ingredient':[{'name':'chili'}]}
        url = details_urls(recipe_id=recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(ingredient2, recipe.ingredient.all())
        self.assertNotIn(ingredient1, recipe.ingredient.all())
    
    def test_clear_recipe_ingredient(self):
        """Test: clearing recipes ingredient"""
        ingredient = Ingredient.objects.create(user=self.user, name='garlic')
        recipe = create_recipe(user=self.user)
        recipe.ingredient.add(ingredient)

        payload = {'ingredient':[]}
        url = details_urls(recipe_id=recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    @patch('recipe.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path"""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        file_path = recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')        
    

class ImageUploadTestCase(TestCase):
    """Test for image upload api"""
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            'user@example.com',
            'password123'
        )
        self.client.force_authenticate(self.user)
        self.recipe = create_recipe(self.user)
    
    def tearDown(self):
        self.recipe.image.delete()
    # main backup
    def test_upload_image(self):
        """Test uploading an image to a recipe."""
        url = image_uploade_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    # test
    # def test_upload_image(self):
    #     url = image_uploade_url(self.recipe.id)
    #     buffer = BytesIO()
    #     Image.new('RGB', (10, 10)).save(buffer, format='JPEG')
    #     buffer.seek(0)
    #     file = SimpleUploadedFile('test.jpg', buffer.read(), content_type='image/jpeg')
    #     res = self.client.post(url, {'image': file}, format='multipart')

    #     # debug
    #     # if res:
    #     #     print(res)
    #     # else:
    #     #     print('no file found')
    #     self.recipe.refresh_from_db()
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertIn('image', res.data)
    #     self.assertTrue(os.path.exists(self.recipe.image.path))

    
    def test_upload_image_bad_request(self):
        """Test: uploading invalid image"""
        url = image_uploade_url(self.recipe.id)
        payload = {'image':'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_filter_by_tag(self):
        """here i am testing with filter with tag"""
        r1 = create_recipe(user=self.user, title='alu vaji')
        r2 = create_recipe(user=self.user, title='alu vorta')
        tag1 = Tag.objects.create(user=self.user, name='vegan')
        tag2 = Tag.objects.create(user=self.user, name='alu')
        r1.tags.add(tag1)
        r2.tags.add(tag2)
        r3 = create_recipe(user=self.user, title='fish and chips')

        params = {'tags': f'{tag1.id}, {tag2.id}'}
        res = self.client.get(RECIPE_URLS, params)

        s1 = RecipeSerializer(r1)
        s2 = RecipeSerializer(r2)
        s3 = RecipeSerializer(r3)

        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)

    def test_filter_by_ingredient(self):
        """test filtering recipe by ingredient""" 
        r1 = create_recipe(user=self.user, title='alu vaji')
        r2 = create_recipe(user=self.user, title='alu vorta')
        in1 = Ingredient.objects.create(user=self.user, name='alu')
        in2 = Ingredient.objects.create(user=self.user, name='oil')
        r1.ingredient.add(in1)
        r2.ingredient.add(in2)
        r3 = create_recipe(user=self.user, title='begun')

        params = {'ingredient': f'{in1.id}, {in2.id}'}
        res = self.client.get(RECIPE_URLS, params)

        s1 = RecipeSerializer(r1)
        s2 = RecipeSerializer(r2)
        s3 = RecipeSerializer(r3)

        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)        
    
    