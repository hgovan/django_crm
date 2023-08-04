from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class CustomUser(AbstractUser):
    phone_number = PhoneNumberField()
    email_validated = models.BooleanField(default=False)
    phone_number_validated = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    credits = models.IntegerField(default=15)

    def get_phone_number(self):
        return self.phone_number

    def __str__(self):
        return self.username
