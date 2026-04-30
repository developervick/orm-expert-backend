from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from courses.models import Course
from users.permissions import IsCreator
from courses.services.course_service import CourseService

course_service = CourseService()


class CourseListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            page = int(request.query_params.get('page', 1))
            courses = course_service.get_paginated_courses(page)
            return Response({"message": "List of courses", "data": courses, "error": None}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"message": "Invalid page number", "data": None, "error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An error occurred", "data": None, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     

class CourseDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            course = course_service.get_course_by_slug(slug)
            if course:
                return Response({"message": "Course details", "data": course, "error": None}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Course not found", "data": None, "error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"message": "Invalid slug", "data": None, "error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An error occurred", "data": None, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CourseCreateView(APIView):
    permission_classes = [IsAuthenticated, IsCreator]

    def post(self, request):

        try:
            # Implement course creation logic here
            name = request.data.get('name')
            slug = request.data.get('slug')
            title = request.data.get('title')
            description = request.data.get('description')
            level = request.data.get('level')
            category = request.data.get('category')
            price = request.data.get('price')
            image_path = request.data.get('image_path')

            course = course_service.create_course(request.user.id, name, slug, title, description, level, category, price, image_path)
            return Response({"message": "Course created successfully", "data": course, "error": None}, status=status.HTTP_201_CREATED)
        except ValueError as ve:
            return Response({"message": str(ve), "data": None, "error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An error occurred", "data": None, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, id):
        try:
            # Implement course update logic here
            course = course_service.get_course_by_id(id)
            if not course:
                return Response({"message": "Course not found", "data": None, "error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

            # Update course details based on request data
            updated_course = course_service.update_course(course.id, **request.data)
            return Response({"message": "Course updated successfully", "data": updated_course, "error": None}, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({"message": str(ve), "data": None, "error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "An error occurred", "data": None, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

