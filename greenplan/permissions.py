from rest_framework import permissions


class IsAuthenticatedOrReadonly(permissions.BasePermission):
    '''An anonymous user can see event that are public from organizers while an organizer 
    can see there own event and other public event'''

    def has_permission(self, request, view):

        if  request.method and request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated)

