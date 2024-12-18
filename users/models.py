from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    USER_CHOICES = [
        ('CANDIDATE', 'Candidate'),
        ('RECRUITER', 'Recruiter'),
    ]

    email = models.EmailField(blank=False, unique=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_CHOICES, default='CANDIDATE')

