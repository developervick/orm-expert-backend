from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from users.models import User

class IsUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role == User.Roles.ADMIN or request.user.role == User.Roles.USER
        return False
            

class IsCreator(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
             return request.user.role == User.Roles.ADMIN or request.user.role == User.Roles.CREATOR
        return False
    

class IsRecruiter(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role == User.Roles.ADMIN or request.user.role == User.Roles.RECRUITER
        return False
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.role == User.Roles.ADMIN
        return False