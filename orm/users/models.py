from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'
        RECRUITER = 'recruiter', 'Recruiter'
        CREATOR = 'creator', "Creator"

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=250, null=False, blank=False, unique=True)
    username = models.CharField(max_length=100, null=False, blank=False, unique=True)
    password = models.CharField(default="no pass")
    phone = models.CharField(max_length=12, null=True, blank=True)
    role = models.CharField(choices=Roles.choices, default=Roles.USER, null=False)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)



class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Permission(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    code_name = models.CharField(max_length=50, name=False)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


class RolePermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Subscription(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    


