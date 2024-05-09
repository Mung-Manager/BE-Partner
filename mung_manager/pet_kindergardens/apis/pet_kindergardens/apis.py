from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mung_manager.apis.mixins import APIAuthMixin
from mung_manager.apis.pagination import LimitOffsetPagination, get_paginated_data
from mung_manager.common.base.serializers import BaseSerializer
from mung_manager.common.constants import SYSTEM_CODE
from mung_manager.common.selectors import get_object_or_not_found
from mung_manager.common.utils import inline_serializer
from mung_manager.pet_kindergardens.containers import PetKindergardenContainer
from mung_manager.pet_kindergardens.enums import (
    ReservationAvailabilityOption,
    ReservationChangeOption,
)


class PetKindergardenCreateAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        name = serializers.CharField(required=True, max_length=64, label="반려동물 유치원 이름")
        main_thumbnail_url = serializers.URLField(
            required=False,
            default="https://s3.ap-northeast-2.amazonaws.com/dev-api.mung-manager.com/default_profile_image.png",
            label="메인 이미지 URL",
        )
        profile_thumbnail_url = serializers.URLField(
            required=False,
            default="https://s3.ap-northeast-2.amazonaws.com/dev-api.mung-manager.com/default_profile_image.png",
            label="프로필 이미지 URL",
        )
        phone_number = serializers.CharField(
            required=False,
            allow_blank=True,
            max_length=16,
            default="",
            label="전화번호",
        )
        visible_phone_number = serializers.ListField(
            required=True,
            child=serializers.CharField(
                max_length=16,
            ),
            max_length=2,
            label="노출 전화번호",
        )
        business_start_hour = serializers.TimeField(required=True, label="영업 시작 시간")
        business_end_hour = serializers.TimeField(required=True, label="영업 종료 시간")
        road_address = serializers.CharField(
            required=True, max_length=128, label="도로명 주소"
        )
        abbr_address = serializers.CharField(
            required=True, max_length=128, label="지번 주소"
        )
        detail_address = serializers.CharField(
            required=False, max_length=128, allow_blank=True, default="", label="상세 주소"
        )
        short_address = serializers.ListField(
            required=True,
            child=serializers.CharField(max_length=128),
            max_length=10,
            label="간단 주소",
        )
        guide_message = serializers.CharField(
            required=False, allow_blank=True, default="", label="안내 메시지"
        )
        reservation_availability_option = serializers.ChoiceField(
            required=True,
            choices=[options.value for options in ReservationAvailabilityOption],
            label="예약 가능 설정",
        )
        reservation_change_option = serializers.ChoiceField(
            required=True,
            choices=[options.value for options in ReservationChangeOption],
            label="예약 변경 옵션",
        )
        daily_pet_limit = serializers.IntegerField(
            required=True,
            min_value=-1,
            max_value=9999,
            label="일일 펫 제한",
            help_text="-1인 경우 전체",
        )

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="반려동물 유치원 아이디")
        name = serializers.CharField(label="반려동물 유치원 이름")
        main_thumbnail_url = serializers.URLField(label="메인 이미지 URL")
        profile_thumbnail_url = serializers.URLField(label="프로필 이미지 URL")
        phone_number = serializers.CharField(label="전화번호")
        visible_phone_number = serializers.ListField(
            child=serializers.CharField(), label="노출 전화번호"
        )
        business_start_hour = serializers.TimeField(label="영업 시작 시간")
        business_end_hour = serializers.TimeField(label="영업 종료 시간")
        road_address = serializers.CharField(label="도로명 주소")
        abbr_address = serializers.CharField(label="지번 주소")
        detail_address = serializers.CharField(label="상세 주소")
        short_address = serializers.ListField(
            child=serializers.CharField(), label="간단 주소"
        )
        guide_message = serializers.CharField(label="안내 메시지")
        reservation_availability_option = serializers.CharField(label="예약 가능 설정")
        reservation_change_option = serializers.CharField(label="예약 변경 옵션")
        daily_pet_limit = serializers.IntegerField(label="일일 펫 제한")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_service = (
            PetKindergardenContainer.pet_kindergarden_service()
        )

    def post(self, request: Request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        pet_kindergarden = self._pet_kindergarden_service.create_pet_kindergarden(
            user=request.user, **input_serializer.validated_data
        )

        pet_kindergarden_data = self.OutputSerializer(pet_kindergarden).data
        return Response(data=pet_kindergarden_data, status=status.HTTP_201_CREATED)


class PetKindergardenSearchAPI(APIAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class FilterSerializer(BaseSerializer):
        name = serializers.CharField(max_length=64, label="반려동물 유치원 이름")
        limit = serializers.IntegerField(
            default=10, min_value=1, max_value=50, label="조회 개수"
        )
        offset = serializers.IntegerField(default=0, min_value=0, label="조회 시작 위치")

    class OutputSerializer(BaseSerializer):
        profile_thumbnail_url = serializers.URLField(
            source="thum_url", label="프로필 이미지 URL"
        )
        name = serializers.CharField(label="이름")
        address = serializers.CharField(label="주소")
        abbr_address = serializers.CharField(label="지번 주소")
        road_address = serializers.CharField(label="도로명 주소")
        phone_number = serializers.CharField(source="tel", label="전화번호")
        short_address = serializers.ListField(
            child=serializers.CharField(), label="간단 주소"
        )
        business_start_hour = serializers.TimeField(label="영업 시작 시간")
        business_end_hour = serializers.TimeField(label="영업 종료 시간")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._raw_pet_kindergarden_selector = (
            PetKindergardenContainer.raw_pet_kindergarden_selector()
        )

    def get(self, request: Request) -> Response:
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
        return Response(
            data=pagination_raw_pet_kindergardens_data, status=status.HTTP_200_OK
        )


class PetKindergardenProfileAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        user = inline_serializer(
            fields={
                "name": serializers.CharField(label="이름"),
            },
            label="유저",
        )
        pet_kindergarden = inline_serializer(
            fields={
                "id": serializers.IntegerField(label="아이디"),
                "name": serializers.CharField(label="이름"),
                "profile_thumbnail_url": serializers.URLField(label="프로필 이미지 URL"),
            },
            label="반려동물 유치원",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = (
            PetKindergardenContainer.pet_kindergarden_selector()
        )

    def get(self, request: Request) -> Response:
        pet_kindergarden = get_object_or_not_found(
            self._pet_kindergarden_selector.get_pet_kindergarden_by_user(
                user=request.user
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        pet_kindergarden_data = self.OutputSerializer(
            {"pet_kindergarden": pet_kindergarden, "user": pet_kindergarden.user}
        ).data
        return Response(data=pet_kindergarden_data, status=status.HTTP_200_OK)
