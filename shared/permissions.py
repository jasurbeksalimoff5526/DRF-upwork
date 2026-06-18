from rest_framework.permissions import SAFE_METHODS, BasePermission

from accounts.models import CLIENT, FREELANCER


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == CLIENT)


class IsFreelancer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == FREELANCER)


class IsClientOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.role == CLIENT)


class IsProjectClient(BasePermission):
    def has_object_permission(self, request, view, obj):
        project = getattr(obj, "project", obj)
        return bool(request.user and request.user.is_authenticated and project.client == request.user)


class IsContractParticipant(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and (obj.client == request.user or obj.freelancer == request.user)
        )


class IsContractClient(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and obj.client == request.user)
