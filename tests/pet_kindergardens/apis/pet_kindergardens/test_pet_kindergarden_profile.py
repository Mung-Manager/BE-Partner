import pytest
from django.urls import reverse

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPetKindergardenProfileAPI(IsAuthenticateTestCase):
    """
    PetKindergardenProfileAPI 테스트 클래스

    - Test List:
        Success:
            - pet_kindergarden_profile_success
        Fail:
            - pet_kindergarden_profile_does_not_exist
            - pet_kindergarden_profile_fail_not_authenticated
            - pet_kindergarden_profile_fail_permission_denied
    """

    url = reverse("api-pet-kindergardens:pet-kindergarden-profile")

    def test_pet_kindergarden_profile_success(self, pet_kindergarden):
        """반려동물 유치원 프로필 조회 성공 테스트

        Args:
            pet_kindergarden : 반려동물 유치원 객체
        """
        access_token = self.obtain_token(pet_kindergarden.user)
        self.authenticate_with_token(access_token)

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.data["data"]["user"]["name"] == pet_kindergarden.user.name
        assert response.data["data"]["pet_kindergarden"]["id"] == pet_kindergarden.id
        assert response.data["data"]["pet_kindergarden"]["name"] == pet_kindergarden.name
        assert response.data["data"]["pet_kindergarden"]["profile_thumbnail_url"] == pet_kindergarden.profile_thumbnail_url

    def test_pet_kindergarden_profile_does_not_exist(self, active_partner_user):
        """반려동물 유치원 프로필 조회 실패 테스트 (존재하지 않는 유치원)

        Args:
            active_partner_user : 활성화된 파트너 유저 객체
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)

        response = self.client.get(self.url)
        assert response.status_code == 404
        assert response.data["code"] == "not_found_pet_kindergarden"
        assert response.data["message"] == "PetKindergarden does not exist."

    def test_pet_kindergarden_profile_fail_not_authenticated(self, pet_kindergarden):
        """반려동물 유치원 프로필 조회 실패 테스트 (인증되지 않은 사용자)

        Args:
            pet_kindergarden : 반려동물 유치원 객체
        """
        response = self.client.get(self.url)
        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_pet_kindergarden_profile_fail_permission_denied(self, active_guest_user):
        """반려동물 유치원 프로필 조회 실패 테스트 (권한 없는 사용자)

        Args:
            active_guest_user : 활성화된 게스트 유저 객체
        """
        access_token = self.obtain_token(active_guest_user)
        self.authenticate_with_token(access_token)

        response = self.client.get(self.url)
        assert response.status_code == 403
        assert response.data["code"] == "permission_denied"
        assert response.data["message"] == "You do not have permission to perform this action."
