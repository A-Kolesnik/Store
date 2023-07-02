from rest_framework.permissions import BasePermission


class ApiUserPermission(BasePermission):

    """Расширяет возможности класса BasePermissions

    Переопределены методы:
        1. has_permission(...)

    """

    def has_permission(self, request, view):
        """Выполняет разграничение доступа по выполняемой операции

        На выполнение операций create/destroy имеют права только админ и персонал
        На выполнение остальных доступных операций, необходимо только авторизация
        """
        if not request.user.is_authenticated:
            return False

        if view.action in ['create', 'destroy'] and not request.user.is_staff:
            return False

        return True
