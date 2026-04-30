
from orm.courses.models import Course

class CourseService:

    def get_all_courses(self):
        """Return all published, non-deleted courses."""
        return Course.objects.filter(published=True)

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