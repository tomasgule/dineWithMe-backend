from rest_framework import permissions

class IsHostOrAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method=="DELETE":
            return False
        if request.method=="GET":
            return True
        return obj.host == request.user


