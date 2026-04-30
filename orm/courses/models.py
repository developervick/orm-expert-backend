from django.db import models
from users.models import User

class Course(models.Model):
    class CourseLevel(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, null=False, unique=True, default="")
    title = models.CharField(max_length=250, null=False, default="")
    description = models.CharField(max_length=500, null=False, default="")
    level = models.CharField(max_length=20, choices=CourseLevel.choices, null=False, default=CourseLevel.BEGINNER)
    category = models.CharField(max_length=500, unique=False, null=False, blank=True, default="")
    rating = models.FloatField(null=False, default=0.0)
    price = models.FloatField(null=False, default=0.0)
    published = models.BooleanField(default=False)
    image_path = models.CharField(max_length=500, null=False, default="")
    updated_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True, blank=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


class CourseMetaData(models.Model):
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    key = models.CharField(max_length=250, null=False)
    value = models.CharField(max_length=500, null=False)
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
