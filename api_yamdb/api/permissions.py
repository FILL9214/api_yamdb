from rest_framework import permissions


class SelfUserPermission(permissions.BasePermission):
    """Обеспечивает доступ к users/me только текущему."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.id == request.user)


class IsUserOrStaffOrReadOnlyPermission(permissions.BasePermission):
    """
    Доступ для автора, модератора и администратора,
    остальным - безопасные методы.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """
    Доступно администратору.
    Для остальных только безопасные методы.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin or request.user.is_superuser)
        return request.method in permissions.SAFE_METHODS


class IsAdminOnlyPermission(permissions.BasePermission):
    """Обеспечивает доступ только администратору."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin or request.user.is_superuser)
        return False
