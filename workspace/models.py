from django.db import models
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()



def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Workspace(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_workspaces")
    unique_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES, default='public')

    def save(self, *args, **kwargs):
        if self.visibility == 'public' and not self.unique_code:
            self.unique_code = generate_unique_code()
        elif self.visibility == 'private':
            self.unique_code = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Membership(models.Model):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("member", "Member"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    can_remove_users = models.BooleanField(default=False) 
    
    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.workspace.name}"