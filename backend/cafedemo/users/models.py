from django.db import models
from datetime import datetime
from django.contrib.auth.hashers import make_password
import django.contrib.auth.hashers as hashers

class User(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=13)
    email = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now, editable=False)
    updated_at = models.DateTimeField(default=datetime.now, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def check_password(self, password):
        return hashers.check_password(password, self.password)
