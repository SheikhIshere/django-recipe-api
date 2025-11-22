"""Custom User model and manager for the system.

This file was reformatted for PEP 8 compliance and improved documentation.
No functional changes were made.
"""

from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin, 
    UserManager
)
from django.db import models


class CustomUserManager(UserManager):
    """Manager for Custom User model, handles user creation."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user.

        Args:
            email (str): Email address of the user.
            password (str, optional): Password for the user. Defaults to None.
            **extra_fields: Additional fields for user creation.

        Returns:
            User: Newly created user instance.

        Raises:
            ValueError: If email is not provided.
        """
        if not email:
            raise ValueError('User must have email')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser with staff and superuser privileges."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model using email as the unique identifier."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
