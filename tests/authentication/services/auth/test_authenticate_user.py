import pytest

from mung_manager.authentication.services.auth import AuthService
from mung_manager.common.exception.exceptions import AuthenticationFailedException


class TestAuthenticateUser:
    """
    AuthService의 authenticate_user 테스트 클래스

    - Test List:
        Success:
            - authenticate_user_success
        Failure:
            - authenticate_user_fail_inactive_user
    """

    def setup_method(self):
        self.auth_service = AuthService()

    def test_authenticate_user_success(self, deleted_partner_user):
        """삭제된 유저 인증 성공 테스트

        Args:
            deleted_partner_user : 삭제된 사장님 유저
        """
        user = self.auth_service.authenticate_user(deleted_partner_user)

        assert not user.is_deleted
        assert user.deleted_at is None
        assert user.last_login is not None

    def test_authenticate_user_fail_inactive_user(self, inactive_partner_user):
        """비활성화된 유저 인증 실패 테스트 (비활성화된 유저)

        Args:
            inactive_partner_user : 비활성화된 사장님 유저
        """
        with pytest.raises(AuthenticationFailedException) as e:
            self.auth_service.authenticate_user(inactive_partner_user)

        assert e.value.detail == "User is not active"
        assert e.value.status_code == 401
