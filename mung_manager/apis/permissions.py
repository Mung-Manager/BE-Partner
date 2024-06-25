from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from mung_manager.users.containers import UserContainer
from mung_manager.users.enums import AuthGroup


class IsPartnerPermission(permissions.BasePermission):

    def __init__(self):
        super().__init__()
        self._group_selector = UserContainer.group_selector()

    def has_permission(self, request: Request, view: APIView):
        """이 함수는 기본적으로 사장님 API에 적용되며, 유저의 권한이 사장님인지 확인합니다.

        Args:
            request (Request): Request 객체
            view (APIView): APIView 객체

        Returns:
            bool: 유저의 권한이 사장님이면 True, 아니면 False를 반환
        """
        try:
            if self._group_selector.exists_by_id_and_user(AuthGroup.PARTNER.value, request.user):
                return True

            return False

        except Exception:
            return False
