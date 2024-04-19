import pytest

from mung_manager.common.exception.exceptions import AuthenticationFailedException
from mung_manager.pet_kindergardens.services.pet_kindergardens import (
    PetKindergardenService,
)

pytestmark = pytest.mark.django_db


class TestGetCoordinatesByRoadAddress:
    """
    PetKindergardenService의 _get_coordinates_by_road_address 테스트 클래스

    - Test List:
        Success:
            - get_coordinates_by_road_address_success
        Fail:
            - get_coordinates_by_road_address_fail
    """

    def setup_method(self):
        self.pet_kindergarden_service = PetKindergardenService()

    def test_get_coordinates_by_road_address_success(self, mocker):
        """도로명 주소로 위도, 경도 조회 성공 테스트

        Args:
            mocker : mocker 객체
        """
        road_address = "서울특별시 강남구 역삼동 123-45"
        latitude = 37.123456
        longitude = 127.123456

        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "documents": [
                {
                    "road_address": {
                        "x": longitude,
                        "y": latitude,
                    },
                }
            ]
        }

        mocker.patch("mung_manager.pet_kindergardens.services.pet_kindergardens.requests.get", return_value=mock_response)

        result = self.pet_kindergarden_service._get_coordinates_by_road_address(road_address)
        assert result == (latitude, longitude)

    def test_get_coordinates_by_road_address_fail(self, mocker):
        """도로명 주소로 위도, 경도 조회 실패 테스트

        Args:
            mocker : mocker 객체
        """
        road_address = "서울특별시 강남구 역삼동 123-45"

        mock_response = mocker.Mock()
        mock_response.status_code = 401

        mocker.patch("mung_manager.pet_kindergardens.services.pet_kindergardens.requests.get", return_value=mock_response)

        with pytest.raises(AuthenticationFailedException) as e:
            self.pet_kindergarden_service._get_coordinates_by_road_address(road_address)

        assert e.value.detail == "Failed to get coordinates from Kakao."
        assert e.value.status_code == 401
