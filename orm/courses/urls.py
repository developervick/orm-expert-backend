from django.urls import path
from courses.views import *

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
]