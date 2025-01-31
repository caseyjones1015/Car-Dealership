from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    GUEST = 'guest'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MODERATOR, 'Moderator'),
        (GUEST, 'Guest'),
        # Add more roles if needed
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=GUEST)
