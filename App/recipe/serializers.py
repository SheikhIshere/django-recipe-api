"""Serializers for the Recipe API app.

This file is reformatted to follow PEP 8 and contains improved
docstrings and comments. No business logic was changed — only style,
readability and documentation.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ingredient, Recipe, Tag


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for Ingredient objects."""

    class Meta:
        model = Ingredient
        fields = ["id", "name"]
        read_only_fields = ["id"]


class TagSerialization(serializers.ModelSerializer):
    """Serializer for Tag objects."""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe list and create/update operations.

    This serializer supports nested tags and ingredients. Helper methods
    are used to get or create associated Tag and Ingredient instances
    when creating or updating a recipe.
    """

    tags = TagSerialization(many=True, required=False)
    ingredient = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "time_minutes",
            "price",
            "link",
            "tags",
            "ingredient",
        ]
        read_only_fields = ["id"]

    def _get_or_create_ingredients(self, ingredient, recipe):
        """Handle getting or creating ingredients as needed.

        Args:
            ingredient (list[dict]): List of ingredient payloads.
            recipe (Recipe): Recipe instance to attach ingredients to.
        """
        auth_user = self.context["request"].user
        for ing in ingredient:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user, **ing
            )
            recipe.ingredient.add(ingredient_obj)

    def _get_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed.

        Note: original name preserved to avoid changing external behaviour.
        """
        auth_user = self.context["request"].user

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)
            recipe.tags.add(tag_obj)

    def create(self, validated_data):
        """Create a new Recipe, creating related tags and ingredients.

        Nested tags and ingredients are optional and will be created if
        provided in the payload.
        """
        tags = validated_data.pop("tags", [])
        ingredient = validated_data.pop("ingredient", [])
        recipe = Recipe.objects.create(**validated_data)

        # Attach created or existing tags and ingredients
        self._get_create_tags(tags=tags, recipe=recipe)
        self._get_or_create_ingredients(ingredient, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update a Recipe instance, handling nested relationships."""
        tags = validated_data.pop("tags", None)
        ingredient = validated_data.pop("ingredient", None)

        if tags is not None:
            instance.tags.clear()
            self._get_create_tags(tags, instance)

        if ingredient is not None:
            instance.ingredient.clear()
            self._get_or_create_ingredients(ingredient, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailsSerializer(RecipeSerializer):
    """Serializer for detailed Recipe view.

    Inherits from RecipeSerializer and adds description and image fields
    used for retrieve/detail endpoints.
    """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description", "image"]


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to a Recipe."""

    class Meta:
        model = Recipe
        fields = ["id", "image"]
        read_only_fields = ["id"]
        extra_kwargs = {"image": {"required": True}}