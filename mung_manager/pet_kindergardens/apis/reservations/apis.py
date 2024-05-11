from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mung_manager.apis.mixins import APIAuthMixin
from mung_manager.common.base.serializers import BaseSerializer
from mung_manager.common.constants import SYSTEM_CODE
from mung_manager.common.selectors import check_object_or_not_found
from mung_manager.common.utils import inline_serializer
from mung_manager.reservations.containers import ReservationContainer


class ReservationCalendarListAPI(APIAuthMixin, APIView):
    class FilterSerializer(BaseSerializer):
        year = serializers.IntegerField(required=True, help_text="년", min_value=0, max_value=2100)
        month = serializers.IntegerField(required=True, help_text="월", min_value=1, max_value=12)

    class OutputSerializer(BaseSerializer):
        daily_reservations = inline_serializer(
            label="일별 예약",
            many=True,
            fields={
                "id": serializers.IntegerField(label="일별 예약 아이디"),
                "time_pet_count": serializers.IntegerField(label="시간별 예약된 펫 수"),
                "all_day_pet_count": serializers.IntegerField(label="하루 동안 예약된 펫 수"),
                "hotel_pet_count": serializers.IntegerField(label="호텔 예약된 펫 수"),
                "reserved_at": serializers.DateField(label="예약 날짜"),
            },
        )
        day_offs = inline_serializer(
            label="휴무일",
            many=True,
            fields={
                "id": serializers.IntegerField(label="휴무일 아이디"),
                "day_off_at": serializers.DateField(label="휴무일 날짜"),
            },
        )
        korea_special_days = inline_serializer(
            label="대한민국 공휴일",
            many=True,
            fields={
                "id": serializers.IntegerField(label="공휴일 아이디"),
                "name": serializers.CharField(label="공휴일 이름"),
                "special_day_at": serializers.DateField(label="공휴일 날짜"),
            },
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._daily_reservation_selector = ReservationContainer.daily_reservation_selector()
        self._pet_kindergarden_selector = ReservationContainer.pet_kindergarden_selector()
        self._day_off_selector = ReservationContainer.day_off_selector()
        self._korea_special_day_selector = ReservationContainer.korea_special_day_selector()

    def get(self, request: Request, pet_kindergarden_id: int) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        check_object_or_not_found(
            self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
                pet_kindergarten_id=pet_kindergarden_id,
                user=request.user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        daily_reservations = (
            self._daily_reservation_selector.get_daily_reservations_queryset_by_year_and_month_and_pet_kindergarden_id(
                year=filter_serializer.validated_data["year"],
                month=filter_serializer.validated_data["month"],
                pet_kindergarden_id=pet_kindergarden_id,
            )
        )
        day_offs = self._day_off_selector.get_day_off_queryset_by_pet_kindergarden_id_and_day_off_at(
            pet_kindergarden_id=pet_kindergarden_id,
            year=filter_serializer.validated_data["year"],
            month=filter_serializer.validated_data["month"],
        )
        korea_special_days = self._korea_special_day_selector.get_korea_special_day_queryset_by_year_and_month(
            year=filter_serializer.validated_data["year"], month=filter_serializer.validated_data["month"]
        )
        daily_reservations_data = self.OutputSerializer(
            {
                "daily_reservations": daily_reservations,
                "day_offs": day_offs,
                "korea_special_days": korea_special_days,
            }
        ).data
        return Response(data=daily_reservations_data, status=status.HTTP_200_OK)


class ReservationDayOffCreateAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        day_off_at = serializers.DateField(required=True, help_text="휴무일 날짜")

    class OutputSerializer(BaseSerializer):
        day_off_at = serializers.DateField(label="휴무일 날짜")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._day_off_service = ReservationContainer.day_off_service()

    def post(self, request: Request, pet_kindergarden_id: int) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        day_off = self._day_off_service.create_day_off(
            pet_kindergarden_id=pet_kindergarden_id,
            day_off_at=input_serializer.validated_data["day_off_at"],
            user=request.user,
        )
        day_off_data = self.OutputSerializer(day_off).data
        return Response(data=day_off_data, status=status.HTTP_201_CREATED)


class ReservationDayOffDeleteAPI(APIAuthMixin, APIView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._day_off_service = ReservationContainer.day_off_service()

    def delete(self, request: Request, pet_kindergarden_id: int, day_off_id: int) -> Response:
        self._day_off_service.delete_day_off(
            pet_kindergarden_id=pet_kindergarden_id,
            day_off_id=day_off_id,
            user=request.user,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
