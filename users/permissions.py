from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    """Проверяет, что пользователь является модератором"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(BasePermission):
    """Проверяет, что пользователь является владельцем"""
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
