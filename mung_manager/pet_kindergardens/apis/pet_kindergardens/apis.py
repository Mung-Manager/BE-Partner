from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mung_manager.common.base.serializers import BaseSerializer
from mung_manager.common.exception.exceptions import NotFoundException
from mung_manager.common.mixins import APIAuthMixin
from mung_manager.common.pagination import LimitOffsetPagination, get_paginated_data
from mung_manager.common.response import create_response
from mung_manager.common.utils import inline_serializer
from mung_manager.pet_kindergardens.containers import PetKindergardenContainer
from mung_manager.pet_kindergardens.enums import (
    ReservationAvailabilityOption,
    ReservationChangeOption,
)


class PetKindergardenCreateAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        name = serializers.CharField(required=True, max_length=64)
        main_thumbnail_url = serializers.URLField(required=True)
        profile_thumbnail_url = serializers.URLField(required=True)
        phone_number = serializers.CharField(
            required=False,
            allow_blank=True,
            max_length=16,
            default="",
        )
        visible_phone_number = serializers.ListField(
            required=True,
            child=serializers.CharField(
                max_length=16,
            ),
            max_length=2,
        )
        business_hours = serializers.CharField(required=True, max_length=16)
        road_address = serializers.CharField(required=True, max_length=128)
        abbr_address = serializers.CharField(required=True, max_length=128)
        detail_address = serializers.CharField(required=False, max_length=128, allow_blank=True, default="")
        short_address = serializers.ListField(required=True, child=serializers.CharField(max_length=128), max_length=10)
        guide_message = serializers.CharField(required=False, allow_blank=True, default="")
        reservation_availability_option = serializers.ChoiceField(
            required=True, choices=[options.value for options in ReservationAvailabilityOption]
        )
        reservation_change_option = serializers.ChoiceField(required=True, choices=[options.value for options in ReservationChangeOption])
        daily_pet_limit = serializers.IntegerField(required=True, min_value=-1, max_value=9999)

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        main_thumbnail_url = serializers.URLField()
        profile_thumbnail_url = serializers.URLField()
        phone_number = serializers.CharField()
        visible_phone_number = serializers.ListField(child=serializers.CharField())
        business_hours = serializers.CharField()
        road_address = serializers.CharField()
        abbr_address = serializers.CharField()
        detail_address = serializers.CharField()
        short_address = serializers.ListField(child=serializers.CharField())
        guide_message = serializers.CharField()
        reservation_availability_option = serializers.CharField()
        reservation_change_option = serializers.CharField()
        daily_pet_limit = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_service = PetKindergardenContainer.pet_kindergarden_service()

    def post(self, request: Request) -> Response:
        """
        유저가 반려동물 유치원을 생성합니다.
        url: /partner/api/v1/pet-kindergardens

        Args:
            InputSerializer: 반려동물 유치원 생성 데이터
                name (str): 이름
                main_thumbnail_url (str): 메인 썸네일 URL
                profile_thumbnail_url (str): 프로필 썸네일 URL
                phone_number (str): 전화번호
                visible_phone_number (List[str]): 노출 전화번호
                business_hours (str): 영업 시간
                road_address (str): 도로명 주소
                abbr_address (str): 지번 주소
                detail_address (str): 상세 주소
                short_address (List[str]): 간단 주소
                guide_message (str): 안내 메시지
                reservation_availability_option (str): 예약 가능 설정
                reservation_change_option (str): 예약 변경 옵션
                daily_pet_limit (int): 일일 펫 제한

        Returns:
            OutSerializer: 반려동물 유치원 정보
                name (str): 이름
                main_thumbnail_url (str): 메인 썸네일 이미지 URL
                profile_thumbnail_url (str): 프로필 이미지 URL
                phone_number (str): 전화번호
                visible_phone_number (List[str]): 노출 전화번호
                business_hours (str): 영업 시간
                road_address (str): 도로명 주소
                abbr_address (str): 지번 주소
                detail_address (str): 상세 주소
                short_address (List[str]): 간단 주소
                guide_message (str): 안내 메시지
                reservation_availability_option (str): 예약 가능 설정
                reservation_change_option (str): 예약 변경 옵션
                daily_pet_limit (int): 일일 펫 제한

        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        pet_kindergarden = self._pet_kindergarden_service.create_pet_kindergarden(user=request.user, **input_serializer.validated_data)

        pet_kindergarden_data = self.OutputSerializer(pet_kindergarden).data
        return create_response(data=pet_kindergarden_data, status_code=status.HTTP_201_CREATED)


class PetKindergardenSearchAPI(APIAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        name = serializers.CharField(max_length=64)
        limit = serializers.IntegerField(default=10, min_value=1, max_value=50)
        offset = serializers.IntegerField(default=0, min_value=0)

    class OutputSerializer(BaseSerializer):
        profile_thumbnail_url = serializers.URLField(source="thum_url")
        name = serializers.CharField()
        address = serializers.CharField()
        abbr_address = serializers.CharField()
        road_address = serializers.CharField()
        phone_number = serializers.CharField(source="tel")
        short_address = serializers.ListField(child=serializers.CharField())
        business_hours = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._raw_pet_kindergarden_selector = PetKindergardenContainer.raw_pet_kindergarden_selector()

    def get(self, request: Request) -> Response:
        """
        유저가 네이버 데이터 반려동물 유치원을 검색합니다.
        url: /partner/api/v1/pet-kindergardens/search

        Args:
            FilterSerializer: 반려동물 유치원 검색 데이터
                name (str): 반려동물 유치원 이름
                limit (int): 조회 개수
                offset (int): 조회 시작 위치

        Returns:
            OutSerializer: 반려동물 유치원 정보
                profile_thumbnail_url (str): 프로필 이미지 URL
                name (str): 이름
                address (str): 주소
                abbr_address (str): 간략 주소
                road_address (str): 도로명 주소
                phone_number (str): 전화번호
                short_address (List[str]): 간략 주소
                business_hours (str): 영업시간
        """
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        raw_pet_kindergardens = self._raw_pet_kindergarden_selector.get_raw_pet_kindergarden_queryset_by_name(
            name=filter_serializer.validated_data["name"]
        )

        pagination_raw_pet_kindergardens_data = get_paginated_data(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=raw_pet_kindergardens,
            request=request,
            view=self,
        )
        return create_response(data=pagination_raw_pet_kindergardens_data, status_code=status.HTTP_200_OK)


class PetKindergardenProfileAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        user = inline_serializer(
            fields={
                "name": serializers.CharField(),
            }
        )
        pet_kindergarden = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
                "profile_thumbnail_url": serializers.URLField(),
            }
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = PetKindergardenContainer.pet_kindergarden_selector()

    def get(self, request: Request) -> Response:
        """
        유저가 반려동물 유치원 프로필을 조회합니다.
        url: /partner/api/v1/pet-kindergardens/profile

        Returns:
            OutSerializer: 반려동물 유치원 정보
                pet_kindergarden (PetKindergarden): 반려동물 유치원 객체
                    id (int): 아이디
                    name (str): 이름
                    profile_thumbnail_url (str): 프로필 이미지 URL
                user (User): 유저 객체
                    name (str): 이름
        """
        pet_kindergarden = self._pet_kindergarden_selector.get_pet_kindergarden_by_user(user=request.user)

        if pet_kindergarden is None:
            raise NotFoundException(detail="PetKindergarden does not exist.", code="not_found_pet_kindergarden")

        pet_kindergarden_data = self.OutputSerializer({"pet_kindergarden": pet_kindergarden, "user": pet_kindergarden.user}).data
        return create_response(data=pet_kindergarden_data, status_code=status.HTTP_200_OK)
