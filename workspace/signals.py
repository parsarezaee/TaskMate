from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Membership, Workspace

@receiver(post_save, sender=Membership)
def update_workspace_owner(sender, instance, **kwargs):
    if instance.role == "owner":
        workspace = instance.workspace
        workspace.owner = instance.user
        workspace.save()
