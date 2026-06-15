from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def set_role_permissions(sender, instance, created, **kwargs):

    if instance.role == "manager":

        group, _ = Group.objects.get_or_create(name="Менеджер")
        instance.groups.add(group)