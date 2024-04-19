import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestUserProfileAPI(IsAuthenticateTestCase):
    """
    UserProfileAPI 테스트 클래스

    - Test List:
        Success:
            - user_profile_success
        Fail:
            - user_profile_fail_not_authenticated
            - user_profile_fail_permission_denied
    """

    url = reverse("api-users:user-profile")

    def test_user_profile_success(self, active_partner_user):
        """유저 프로필 조회 성공 테스트

        Args:
            active_partner_user : 활성화된 사장님 유저
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"]["name"] == active_partner_user.name
        assert response.data["data"]["email"] == active_partner_user.email
        assert response.data["data"]["phone_number"] == active_partner_user.phone_number

    def test_user_profile_fail_not_authenticated(self):
        """유저 프로필 조회 실패 테스트 (인증되지 않은 사용자)"""
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_user_profile_fail_permission_denied(self, active_guest_user):
        """유저 프로필 조회 실패 테스트 (권한 없는 사용자)

        Args:
            active_guest_user : 활성화된 손님 유저
        """
        access_token = self.obtain_token(active_guest_user)
        self.authenticate_with_token(access_token)
        response = self.client.get(self.url)

        assert response.status_code == 403
        assert response.data["code"] == "permission_denied"
        assert response.data["message"] == "You do not have permission to perform this action."
