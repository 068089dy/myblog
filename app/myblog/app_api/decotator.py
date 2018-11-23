from functools import update_wrapper


def wrap_permission(*permissions, validate_permission=True):
    """custom permissions for special route"""
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            self.permission_classes = permissions
            if validate_permission:
                self.check_permissions(request)
            return func(self, request, *args, **kwargs)
        return update_wrapper(wrapper, func)
    return decorator
