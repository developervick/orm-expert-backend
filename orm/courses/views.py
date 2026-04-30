from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from courses.models import Course
from users.permissions import IsCreator


class CourseListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = 10
        offset = (page - 1) * page_size
        courses = Course.objects.filter(deleted_at=None).values('id', 'name', 'slug', 'title', 'description', 'level', 'category')[offset:offset + page_size]
        return Response({"message": "List of courses", "data": courses, "error": None}, status=status.HTTP_200_OK)
    

class CourseCreateView(APIView):
    permission_classes = [IsAuthenticated, IsCreator]

    def post(self, request):
        # Implement course creation logic here
        return Response({"message": "Course created successfully", "data": None, "error": None}, status=status.HTTP_201_CREATED)

