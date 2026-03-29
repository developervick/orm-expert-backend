from django.db import models
from users.models import User

class Course(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=500, unique=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Module(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Chapter(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, null=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Exercise(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
