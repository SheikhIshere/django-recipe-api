"""url mapping for recipe app"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RecipeViewset,
    TagViewSet,
    IngredientViewset
)


router = DefaultRouter()
router.register('recipe', RecipeViewset)
router.register('tags', TagViewSet)
router.register('ingredient', IngredientViewset)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]