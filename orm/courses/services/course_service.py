
from courses.models import Course

class CourseService:

    def get_paginated_courses(self, page: int = 1, page_size: int = 10):
        """Return all published, non-deleted courses."""
        offset = (page - 1) * page_size
        return Course.objects.filter(published=True)[offset:offset + page_size]

    def get_course_by_slug(self, slug: str):
        """
        Fetch a single course by slug.
        Returns None if not found — let the view decide what HTTP status to send.
        """
        try:
            return Course.objects.get(slug=slug)
        except Course.DoesNotExist:
            return None

    def get_courses_by_level(self, level: str):
        """Filter courses by difficulty level."""
        return Course.objects.filter(
            published=True,
            level=level
        )

    def get_courses_by_instructor(self, user_id: int):
        """All courses belonging to a specific instructor."""
        return Course.objects.filter(user_id=user_id)
    

class CourseCreateService():

    def create_course(self, user_id: int, name: str, slug: str, title: str, description: str, level: str, category: str, price: float, image_path: str):
        """Create a new course with the given details."""

        if Course.objects.filter(name=name).exists():
            raise ValueError("Course with this name already exists.")
        
        if Course.objects.filter(slug=slug).exists():
            raise ValueError("Course with this slug already exists.")

        course = Course.objects.create(
            user_id=user_id,
            name=name,
            slug=slug,
            title=title,
            description=description,
            level=level,
            category=category,
            price=price,
            image_path=image_path
        )
        return course
    

    def update_course(self, course_id: int, **kwargs):
        """Update an existing course with the provided details."""
        try:
            course = Course.objects.get(id=course_id)
            for key, value in kwargs.items():
                setattr(course, key, value)
            course.save()
            return course
        except Course.DoesNotExist:
            raise ValueError("Course not found.")