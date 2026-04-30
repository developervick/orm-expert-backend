from django.db import models
from users.models import User

class SoftDeleteManager(models.Manager):
    """Returns only records that haven't been soft-deleted."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)
    

class SoftDeleteModel(models.Model):
    """Abstract base — gives every model timestamps + soft delete for free."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # escape hatch when you need deleted records too

    class Meta:
        abstract = True

    def soft_delete(self):
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])



class Course(SoftDeleteModel):
    class CourseLevel(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    slug = models.SlugField(max_length=250, null=False, unique=True, default="")
    title = models.CharField(max_length=250, null=False, default="")
    description = models.CharField(max_length=500, null=False, default="")
    level = models.CharField(max_length=20, choices=CourseLevel.choices, null=False, default=CourseLevel.BEGINNER)
    category = models.CharField(max_length=500, unique=False, null=False, blank=True, default="")
    rating = models.FloatField(null=False, default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    published = models.BooleanField(default=False)
    image_path = models.CharField(max_length=500, null=False, default="")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name

class CourseMetaData(SoftDeleteModel):
    id = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_metadata')
    key = models.CharField(max_length=250, null=False)
    value = models.CharField(max_length=500, null=False)

    class Meta:
        ordering = ['created_at']

class Module(SoftDeleteModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    order = models.IntegerField(null=False, default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.name} | {self.name}"


class Chapter(SoftDeleteModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, null=False, default="")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='chapters')
    order = models.IntegerField(null=False, default=0)

    class Meta:
        ordering = ['order']   
    
    def __str__(self):
        return f"{self.module.course.name} |{self.module.name} | {self.name}"


class Exercise(SoftDeleteModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250, null=False)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='exercises', default=None)
    order = models.IntegerField(null=False, default=0)

    class Meta:
        ordering = ['order']    

    def __str__(self):        
        return f"{self.chapter.module.course.name} | {self.chapter.module.name} | {self.chapter.name} | {self.name}"
    


class CourseRating(SoftDeleteModel):
    """Source of truth for ratings. Compute avg in the service layer."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField()  # 1–5, validate in serializer/service

    class Meta:
        unique_together = ('course', 'user')  # one rating per user per course

    def __str__(self):
        return f"{self.user} rated {self.course.name}: {self.score}"
