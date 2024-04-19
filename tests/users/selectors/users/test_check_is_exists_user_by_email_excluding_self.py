import pytest

from mung_manager.users.selectors.users import UserSelector

pytestmark = pytest.mark.django_db


class TestCheckIsExistsUserByEmailExcludingSelf:
    """
    UserSelector의 check_is_exists_user_by_email_excluding_self 테스트 클래스

    - Test List:
        Success:
            - check_is_exists_user_by_email_excluding_self_success_is_exists_false
            - check_is_exists_user_by_email_excluding_self_success_is_exists_true
    """

    def setup_method(self):
        self.user_selector = UserSelector()

    def check_is_exists_user_by_email_excluding_self_success_is_exists_false(self, active_partner_user):
        """이메일로 자신을 제외한 유저 조회 성공 테스트

        Args:
            active_partner_user : 활성화된 사장님 유저
        """
        is_exists = self.user_selector.check_is_exists_user_by_email_excluding_self(
            email=active_partner_user.email, user=active_partner_user
        )
        assert is_exists is False

    def test_check_is_exists_user_by_email_excluding_self_success_is_exists_true(self, active_partner_user, active_guest_user):
        """이메일로 자신을 제외한 유저 조회 성공 테스트 (존재하는 이메일)

        Args:
            active_partner_user : 활성화된 사장님 유저
            active_guest_user : 활성화된 손님 유저
        """
        is_exists = self.user_selector.check_is_exists_user_by_email_excluding_self(email=active_guest_user.email, user=active_partner_user)
        assert is_exists is True
