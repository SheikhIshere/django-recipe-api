"""Models for the Recipe API app.

This version is formatted for PEP 8 and includes improved docstrings.
No business logic or field definitions were changed.
"""

import os
import uuid
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


def recipe_image_file_path(instance, filename):
    """Generate file path for uploaded recipe images.

    Args:
        instance: The model instance the file is associated with.
        filename (str): Original filename.

    Returns:
        str: A unique, UUID-based path for storing the uploaded image.
    """
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "recipe", filename)


class Recipe(models.Model):
    """Core Recipe model.

    Stores recipe metadata, relational links to tags and ingredients,
    and supports image uploads.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    tags = models.ManyToManyField("Tag")
    ingredient = models.ManyToManyField("Ingredient")
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag model used for categorizing recipes."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient model representing recipe components."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name