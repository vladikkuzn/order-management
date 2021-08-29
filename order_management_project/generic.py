from rest_framework.permissions import BasePermission


def method_permission_classes(permission_classes: tuple):
    """
    Class method decorator to restrict permission classes to :param:permission_classes
    """
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            default_permission_classes = tuple(self.permission_classes)  # save default permission_classes
            self.permission_classes = permission_classes
            self.check_permissions(self.request)
            result = func(self, *args, **kwargs)
            self.permission_classes = default_permission_classes   # restore default permission_classes
            return result
        return decorated_func
    return decorator
