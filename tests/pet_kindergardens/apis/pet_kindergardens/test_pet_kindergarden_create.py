import pytest
from django.urls import reverse

from mung_manager.pet_kindergardens.enums import (
    ReservationAvailabilityOption,
    ReservationChangeOption,
)
from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestPetKindergardenCreateAPI(IsAuthenticateTestCase):
    """
    PetKindergardenCreate의 테스트 클래스

    - Test List:
        Success:
            - pet_kindergarden_create_success
        Fail:
            - pet_kindergarden_create_fail_not_authenticated
            - pet_kindergarden_create_fail_permission_denied
            - pet_kindergarden_create_fail_phone_number_validation
            - pet_kindergarden_create_fail_reservation_availability_option_invalid_choice
            - pet_kindergarden_create_fail_reservation_change_option_invalid_choice
    """

    url = reverse("api-pet-kindergardens:pet-kindergarden-list")

    def test_pet_kindergarden_create_success(self, active_partner_user, mocker):
        """반려동물 유치원 생성 성공 테스트

        Args:
            active_partner_user : 활성화된 파트너 유저 객체
            mocker : mocker 객체
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)

        mocker.patch(
            "mung_manager.pet_kindergardens.services.pet_kindergardens.PetKindergardenService._get_coordinates_by_road_address",
            return_value=(90, 180),
        )

        pet_kindergarden_data = {
            "name": "test",
            "main_thumbnail_url": "https://test.com",
            "profile_thumbnail_url": "https://test.com",
            "phone_number": "010-1234-5678",
            "visible_phone_number": ["010-1234-5678"],
            "business_hours": "09:00 ~ 18:00",
            "abbr_address": "서울특별시 강남구",
            "road_address": "서울특별시 강남구",
            "detail_address": "서울특별시 강남구",
            "short_address": ["서울특별시 강남구"],
            "guide_message": "test",
            "reservation_availability_option": ReservationAvailabilityOption.TODAY.value,
            "reservation_change_option": ReservationChangeOption.TODAY.value,
            "daily_pet_limit": 10,
        }

        response = self.client.post(
            self.url,
            data=pet_kindergarden_data,
            format="json",
        )

        assert response.status_code == 201
        assert response.data["data"]["name"] == pet_kindergarden_data["name"]
        assert response.data["data"]["main_thumbnail_url"] == pet_kindergarden_data["main_thumbnail_url"]
        assert response.data["data"]["profile_thumbnail_url"] == pet_kindergarden_data["profile_thumbnail_url"]
        assert response.data["data"]["phone_number"] == pet_kindergarden_data["phone_number"]
        assert response.data["data"]["visible_phone_number"] == pet_kindergarden_data["visible_phone_number"]
        assert response.data["data"]["business_hours"] == pet_kindergarden_data["business_hours"]
        assert response.data["data"]["abbr_address"] == pet_kindergarden_data["abbr_address"]
        assert response.data["data"]["road_address"] == pet_kindergarden_data["road_address"]
        assert response.data["data"]["detail_address"] == pet_kindergarden_data["detail_address"]
        assert response.data["data"]["reservation_availability_option"] == pet_kindergarden_data["reservation_availability_option"]
        assert response.data["data"]["reservation_change_option"] == pet_kindergarden_data["reservation_change_option"]
        assert response.data["data"]["daily_pet_limit"] == pet_kindergarden_data["daily_pet_limit"]

    def test_pet_kindergarden_create_fail_not_authenticated(self):
        """반려동물 유치원 생성 실패 테스트 (인증되지 않은 사용자)"""
        response = self.client.post(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_pet_kindergarden_create_fail_permission_denied(self, active_guest_user):
        """반려동물 유치원 생성 실패 테스트 (권한 없는 사용자)

        Args:
            active_guest_user : 활성화된 손님 유저 객체
        """
        access_token = self.obtain_token(active_guest_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(self.url)

        assert response.status_code == 403
        assert response.data["code"] == "permission_denied"
        assert response.data["message"] == "You do not have permission to perform this action."

    def test_pet_kindergarden_create_fail_reservation_availability_option_invalid_choice(self, active_partner_user, mocker):
        """반려동물 유치원 생성 실패 테스트 (예약 가능 설정 선택지가 아닌 경우)

        Args:
            active_partner_user : 활성화된 파트너 유저 객체입니다.
            mocker : mocker 객체입니다.
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)

        pet_kindergarden_data = {
            "name": "test",
            "main_thumbnail_url": "https://test.com",
            "profile_thumbnail_url": "https://test.com",
            "phone_number": "010-1234-5678",
            "visible_phone_number": ["010-1234-5678"],
            "business_hours": "09:00 ~ 18:00",
            "abbr_address": "서울특별시 강남구",
            "road_address": "서울특별시 강남구",
            "detail_address": "서울특별시 강남구",
            "short_address": ["서울특별시 강남구"],
            "guide_message": "test",
            "reservation_availability_option": "test",
            "reservation_change_option": ReservationChangeOption.TODAY.value,
            "daily_pet_limit": 10,
        }

        response = self.client.post(
            self.url,
            data=pet_kindergarden_data,
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"reservation_availability_option": ['"test" is not a valid choice.']}

    def test_pet_kindergarden_create_fail_reservation_change_option_invalid_choice(self, active_partner_user):
        """반려동물 유치원 생성 실패 테스트 (예약 변경 옵션 선택지가 아닌 경우)

        Args:
            active_partner_user : 활성화된 파트너 유저 객체
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)

        pet_kindergarden_data = {
            "name": "test",
            "main_thumbnail_url": "https://test.com",
            "profile_thumbnail_url": "https://test.com",
            "phone_number": "010-1234-5678",
            "visible_phone_number": ["010-1234-5678"],
            "business_hours": "09:00 ~ 18:00",
            "abbr_address": "서울특별시 강남구",
            "road_address": "서울특별시 강남구",
            "detail_address": "서울특별시 강남구",
            "short_address": ["서울특별시 강남구"],
            "guide_message": "test",
            "latitude": 90,
            "longitude": 180,
            "reservation_availability_option": ReservationAvailabilityOption.TODAY.value,
            "reservation_change_option": "test",
            "daily_pet_limit": 10,
        }

        response = self.client.post(
            self.url,
            data=pet_kindergarden_data,
            format="json",
        )

        assert response.status_code == 400
        assert response.data["code"] == "invalid_parameter_format"
        assert response.data["message"] == {"reservation_change_option": ['"test" is not a valid choice.']}
