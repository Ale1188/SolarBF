from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('worker', 'Worker'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='members'
    )

    def __str__(self):
        return self.username
