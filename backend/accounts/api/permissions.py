from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    message = "you have already logged in!"

    def has_permission(self, request, view):
        return request.user.is_anonymous


class IsAuthenticated(BasePermission):
    message = "you are anonymouse user!"

    def has_permission(self, request, view):
        return request.user.is_authenticated
