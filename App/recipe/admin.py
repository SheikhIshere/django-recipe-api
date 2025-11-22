"""Admin registrations for Recipe API models.

Reformatted for PEP 8 compliance and improved documentation.
Logic remains unchanged.
"""

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Ingredient, Recipe, Tag


@admin.register(Recipe)
class RecipeAdminModel(ModelAdmin):
    """Admin configuration for Recipe objects.

    Provides list display fields for quick visibility of key attributes.
    """

    list_display = [
        "id",
        "user",
        "title",
        "time_minutes",
        "price",
    ]


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    """Admin configuration for Tag objects."""

    list_display = [
        "id",
        "user",
        "name",
    ]


@admin.register(Ingredient)
class IngredientAdmin(ModelAdmin):
    """Admin configuration for Ingredient objects."""

    list_display = [
        "id",
        "user",
        "name",
    ]