from rest_framework import permissions

from greenplan.models import Event, Template,Organizer


class IsAdminOrReadonly(permissions.BasePermission):
    '''allow admin to perform operation such as post,patch,put,delete'''

    def has_permission(self, request, view):
        if  request.method and request.method not in permissions.SAFE_METHODS:
            return bool(request.user.is_authenticated and request.user.is_staff )
        return True

class IsOrganizerOrReadOnly(permissions.BasePermission):
    '''Allows organizer or staff to update and delete object'''

    def has_permission(self, request, view):
        '''Allow everyone to see an event and only staff can perform all action'''
        if request.method and request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        '''Allow organizer and staff to perform edit and other methods'''

        user = request.user
        
        organizer = None
        if isinstance(obj,Organizer):
            organizer = obj.user
        if isinstance(obj,Event):
            organizer = obj.organizer.user
        if isinstance(obj,Template):
            organizer = obj.owner.user
        
        return  user.is_staff  or organizer == user

