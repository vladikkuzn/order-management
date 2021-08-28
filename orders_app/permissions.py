from rest_framework.permissions import BasePermission
from users_app.enums import Role


class OrderCreate(BasePermission):
    """
    Permission class to give user with allowed_roles create new Order instance.
    """

    allowed_roles = (Role.CASHIER,)
    allowed_methods = ('POST',)

    def has_permission(self, request, view):
        if request.method in self.allowed_methods:
            return request.user.role in self.allowed_roles
        return False


class OrderView(BasePermission):
    """
    Permission class to give user with allowed_roles view Order instance.
    """

    allowed_roles = (Role.SALES_CONSULTANT, Role.ACCOUNTANT)
    allowed_methods = ('GET',)

    def has_permission(self, request, view):
        if request.method in self.allowed_methods:
            return request.user.role in self.allowed_roles
        return False


class OrderStatusChange(BasePermission):
    """
    Permission class to give user with allowed_roles change status of Order instance.
    """

    allowed_roles = (Role.SALES_CONSULTANT, Role.CASHIER)
    allowed_methods = ('PATCH',)

    def has_permission(self, request, view):
        if request.method in self.allowed_methods and self._status_is_present(request.data):
            return request.user.role in self.allowed_roles
        return False

    @staticmethod
    def _status_is_present(data: dict) -> bool:
        return data.get('status')


class GenerateBill(BasePermission):
    """
    Permission class to give user with allowed_roles create and view Bill instance.
    """

    allowed_roles = (Role.CASHIER,)
    allowed_methods = ('GET', 'POST')

    def has_permission(self, request, view):
        if request.method in self.allowed_methods:
            return request.user.role in self.allowed_roles
        return False
