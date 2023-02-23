from rest_framework import permissions


class GuestOrAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )