from rest_framework import permissions


class IsAnonymous(permissions.BasePermission):
    ''' Custom permission to only allow access to anonymous user(unauthenticated users).'''

    def has_permission(self, request, view):
        return not bool(request.user.is_authenticated)
