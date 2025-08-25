from rest_framework.permissions import BasePermission, SAFE_METHODS


# PUBLIC_INTERFACE
class IsOwnerOrReadOnly(BasePermission):
    """Allow owners to edit/delete their objects, read-only for others."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.owner == request.user  # even reads restricted to owner
        return obj.owner == request.user
