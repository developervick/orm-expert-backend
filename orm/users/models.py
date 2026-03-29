from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=250, null=False, blank=False, unique=True)
    username = models.CharField(max_length=100, null=False, blank=False, unique=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
