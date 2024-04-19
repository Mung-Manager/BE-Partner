import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPetKindergardenSearchAPI(IsAuthenticateTestCase):
    """
    PetKindergardenSearchAPI 테스트 클래스

    - Test List:
        Success:
            - pet_kindergarden_search_success
        Fail:
            - pet_kindergarden_search_fail_not_authenticated
            - pet_kindergarden_search_fail_permission_denied
    """

    url = reverse("api-pet-kindergardens:pet-kindergarden-search")

    def test_pet_kindergarden_search_success(self, active_partner_user, raw_pet_kindergarden):
        """반려동물 유치원 검색 조회 성공 테스트

        Args:
            active_partner_user : 활성화된 파트너 유저 객체
            raw_pet_kindergarden : 로우 반려동물 유치원 객체
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)

        response = self.client.get(
            self.url,
            data={"name": raw_pet_kindergarden.name, "limit": 1, "offset": 0},
        )

        assert response.status_code == 200
        assert response.data["data"]["count"] == 1
        assert response.data["data"]["results"][0]["name"] == raw_pet_kindergarden.name
        assert response.data["data"]["results"][0]["profile_thumbnail_url"] == raw_pet_kindergarden.thum_url
        assert response.data["data"]["results"][0]["name"] == raw_pet_kindergarden.name
        assert response.data["data"]["results"][0]["address"] == raw_pet_kindergarden.address
        assert response.data["data"]["results"][0]["abbr_address"] == raw_pet_kindergarden.abbr_address
        assert response.data["data"]["results"][0]["road_address"] == raw_pet_kindergarden.road_address
        assert response.data["data"]["results"][0]["phone_number"] == raw_pet_kindergarden.tel
        assert response.data["data"]["results"][0]["business_hours"] == raw_pet_kindergarden.business_hours
        assert response.data["data"]["results"][0]["short_address"] == raw_pet_kindergarden.short_address

    def test_pet_kindergarden_search_fail_not_authenticated(self):
        """반려동물 유치원 검색 조회 실패 테스트 (인증되지 않은 사용자)"""
        response = self.client.get(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_pet_kindergarden_search_fail_permission_denied(self, active_guest_user):
        """반려동물 유치원 검색 조회 실패 테스트 (권한 없는 사용자)

        Args:
            active_guest_user : 활성화된 게스트 유저 객체
        """
        access_token = self.obtain_token(active_guest_user)
        self.authenticate_with_token(access_token)

        response = self.client.get(self.url)

        assert response.status_code == 403
        assert response.data["code"] == "permission_denied"
        assert response.data["message"] == "You do not have permission to perform this action."
