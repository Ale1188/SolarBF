from django.db.models.signals import post_save, post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'user':
            group = Group.objects.get(name='User')
        elif instance.role == 'worker':
            group = Group.objects.get(name='Worker')
        elif instance.role == 'admin':
            group = Group.objects.get(name='Admin')
        instance.groups.add(group)

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    user_group, created = Group.objects.get_or_create(name='User')
    worker_group, created = Group.objects.get_or_create(name='Worker')
    admin_group, created = Group.objects.get_or_create(name='Admin')
