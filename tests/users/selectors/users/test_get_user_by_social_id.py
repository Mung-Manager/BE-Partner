import pytest

from mung_manager.users.selectors.users import UserSelector

pytestmark = pytest.mark.django_db


class TestGetUserBySocialId:
    """
    UserSelector의 get_user_by_social_id 테스트 클래스

    - Test List:
        Success:
            - get_user_by_social_id_success
        Fail:
            - get_user_by_social_id_fail_does_not_exist
    """

    def setup_method(self):
        self.user_selector = UserSelector()

    def test_get_user_by_social_id_success(self, active_partner_user):
        """소셜 아이디로 유저 조회 성공 테스트

        Args:
            active_partner_user : 활성화된 사장님 유저
        """
        user = self.user_selector.get_user_by_social_id(active_partner_user.social_id)
        assert user == active_partner_user

    def test_get_user_by_social_id_fail_does_not_exist(self):
        """소셜 아이디로 유저 조회 실패 테스트 (존재하지 않는 유저)"""
        user = self.user_selector.get_user_by_social_id("test")
        assert user is None
