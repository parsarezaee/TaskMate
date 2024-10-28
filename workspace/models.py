from django.db import models
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()



def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Workspace(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_workspaces")
    unique_code = models.CharField(max_length=6, unique=True, default=generate_unique_code)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[("admin", "Admin"), ("member", "Member")])

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.Workspace.name}"