#models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

class RoomUserManager(BaseUserManager):
    def create_user(self, room_id, username, registry_email, password=None, **extra_fields):
        # Validate mandatory fields
        if not room_id:
            raise ValueError("The Room ID field must be set.")
        if not username:
            raise ValueError("The Username field must be set.")
        if not registry_email:
            raise ValueError("The Email field must be set.")

        # Normalize email and username
        registry_email = self.normalize_email(registry_email)
        username = self.model.normalize_username(username)

        # # Check if room ID already exists
        # if RoomUser.objects.filter(room_id=room_id).exists():
        #     raise ValueError("A user with this Room ID already exists.")

        # Check if username or email already exists
        if RoomUser.objects.filter(username=username).exists():
            raise ValueError("A user with this Username already exists.")
        if RoomUser.objects.filter(registry_email=registry_email).exists():
            raise ValueError("A user with this Email already exists.")

        # Create the user
        extra_fields.setdefault('is_active', True)  # Ensure 'is_active' is set by default
        user = self.model(
            room_id=room_id,
            username=username,
            registry_email=registry_email,
            **extra_fields
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)  # Save to the database
        return user
