from rest_framework import permissions

from apps.user.manager import ADMIN, STAFF, CLIENT, GUEST


class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class UserIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and\
               request.user.get_type_display() == ADMIN


class UserIsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and\
               request.user.get_type_display() in (ADMIN, STAFF)


class UserIsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and\
               request.user.get_type_display() in CLIENT


class UserIsGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and\
               request.user.get_type_display() in GUEST
