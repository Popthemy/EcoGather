from rest_framework import permissions

from greenplan.models import Event, Template, Organizer, Address


class IsAdminOrReadonly(permissions.BasePermission):
    '''allow admin to perform operation such as post,patch,put,delete'''

    def has_permission(self, request, view):
        if request.method and request.method not in permissions.SAFE_METHODS:
            return bool(request.user.is_authenticated and request.user.is_staff)
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
        if isinstance(obj, Organizer):
            organizer = obj.user
            # print(f' #$#$# This is an organizer object: {obj.user} {user}')

        if  isinstance(obj, Address) :
            ''' used obj[0] incase of list view to get a single view to try it with'''
            print('&&& from permission is organizer or read only &&&')
            organizer = obj.organizer.user

        if isinstance(obj, Event):
            organizer = obj.organizer.user

        if isinstance(obj, Template):
            organizer = obj.owner.user

        return bool(user.is_staff or organizer == user)

class IsOrganizerOwnerOrReadOnly(permissions.BasePermission):
    """
        Allows other users to view objects, but restricts creation to owners or admins.
        Owner is the person that the current object we are viewing belongs to.
    """

    def has_permission(self, request, view):

        if request.method not in permissions.SAFE_METHODS:
            if 'organizer_pk' in view.kwargs:
                org_pk = view.kwargs.get('organizer_pk')
                user = request.user

                return user.is_staff or user.id == org_pk

        return True # the safe method everyone has permission to them
    
    def has_object_permission(self, request, view, obj):
        '''this will only work if an object exist already'''

        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        organizer = obj.organizer.user

        return user.is_staff or organizer == user
