from math import floor
from typing import List, Tuple

import requests
from django.conf import settings
from django.contrib.gis.geos import Point
from django.db import transaction

from mung_manager.common.exception.exceptions import (
    AlreadyExistsException,
    AuthenticationFailedException,
)
from mung_manager.pet_kindergardens.models import PetKindergarden
from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)


class PetKindergardenService:
    """
    이 클래스는 반려동물 유치원과 관련된 비즈니스 로직을 담당합니다.
    """

    def __init__(self, pet_kindergarden_selector: PetKindergardenSelector):
        self._pet_kindergarden_selector = pet_kindergarden_selector

    def _get_coordinates_by_road_address(self, road_address: str) -> Tuple[float, float]:
        """
        이 함수는 도로명 주소를 받아 위도, 경도를 얻어옵니다.

        Args:
            road_address (str): 도로명 주소

        Returns:
            Tuple[float, float]: 위도, 경도
        """
        response = requests.get(
            url="https://dapi.kakao.com/v2/local/search/address.json",
            headers={"Authorization": f"KakaoAK {settings.KAKAO_API_KEY}"},
            params={  # type: ignore
                "analyze_type": "exact",
                "query": road_address,
                "page": 1,
                "size": 1,
            },
        )
        if response.status_code != 200:
            raise AuthenticationFailedException("Failed to get coordinates from Kakao.")

        response_data = response.json()

        latitude = floor(float(response_data["documents"][0]["road_address"]["y"]) * 10**6) / 10**6
        longitude = floor(float(response_data["documents"][0]["road_address"]["x"]) * 10**6) / 10**6

        return latitude, longitude

    @transaction.atomic
    def create_pet_kindergarden(
        self,
        user,
        name: str,
        profile_thumbnail_url: str,
        phone_number: str,
        visible_phone_number: List[str],
        business_hours: str,
        road_address: str,
        abbr_address: str,
        detail_address: str,
        short_address: List[str],
        guide_message: str,
        reservation_availability_option: str,
        reservation_change_option: str,
        daily_pet_limit: int,
        main_thumbnail_url: str,
    ) -> PetKindergarden:
        """
        이 함수는 반려동물 유치원 데이터를 받아 반려동물 유치원을 생성합니다.

        Args:
            user (User): 유저 객체
            name (str): 반려동물 유치원 이름
            profile_thumbnail_url (str): 프로필 썸네일 URL
            phone_number (str): 전화번호
            visible_phone_number (List[str]): 보이는 전화번호
            business_hours (str): 영업시간
            road_address (str): 도로명 주소
            abbr_address (str): 간략 주소
            detail_address (str): 상세 주소
            short_address (list[str]): 짧은 주소
            guide_message (str): 가이드 메시지
            reservation_availability_option (str): 예약 가능 설정
            reservation_change_option (str): 예약 변경 옵션
            daily_pet_limit (int): 일일 반려동물 제한
            main_thumbnail_url (str): 메인 썸네일 URL

        Returns:
            PetKindergarden: 반려동물 유치원 객체
        """
        if self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_user(user):
            raise AlreadyExistsException("User already has a pet kindergarden.")

        # 도로명 주소로 위도, 경도를 조회
        latitude, longitude = self._get_coordinates_by_road_address(road_address)

        pet_kindergarden = PetKindergarden.objects.create(
            name=name,
            profile_thumbnail_url=profile_thumbnail_url,
            main_thumbnail_url=main_thumbnail_url,
            phone_number=phone_number,
            visible_phone_number=visible_phone_number,
            business_hours=business_hours,
            road_address=road_address,
            abbr_address=abbr_address,
            detail_address=detail_address,
            short_address=short_address,
            guide_message=guide_message,
            latitude=latitude,
            longitude=longitude,
            point=Point(longitude, latitude),
            reservation_availability_option=reservation_availability_option,
            reservation_change_option=reservation_change_option,
            daily_pet_limit=daily_pet_limit,
            user=user,
        )

        return pet_kindergarden
