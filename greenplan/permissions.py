from rest_framework import permissions


class IsAdminOrReadonly(permissions.BasePermission):
    '''allow admin to perform operation such as post,patch,put,delete'''

    def has_permission(self, request, view):
        if  request.method and request.method not in permissions.SAFE_METHODS:
            return bool(request.user.is_authenticated and request.user.is_staff )
        return True

class IsOrganizerOrAdmin(permissions.BasePermission):
    '''An organizer has the right to edit only object that belong to them'''

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff or user == obj.organizer:
            return True
        return False
