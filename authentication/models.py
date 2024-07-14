
from typing import Any
from django.db import models
from helpers.models import TrackingModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.conf import settings
import jwt
from datetime import datetime, timedelta
# Create your models here.

class MyUserManager(UserManager):
    
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given name must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        return self._create_user(username, email, password, **extra_fields)
        

class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=150, validators=[username_validator], unique=True)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    # is_active = models.BooleanField(default=True)
    
    objects = MyUserManager()
    
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def token(self):
        token = jwt.encode(
            {
                "username":self.username,
                "email": self.email,
                "expiry":(datetime.utcnow() + timedelta(seconds=60)).isoformat()
            }, settings.SECRET_KEY, algorithm="HS256")
        
        return token