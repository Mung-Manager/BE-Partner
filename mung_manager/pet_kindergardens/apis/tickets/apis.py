from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mung_manager.apis.mixins import APIAuthMixin
from mung_manager.common.base.serializers import BaseSerializer
from mung_manager.common.constants import SYSTEM_CODE
from mung_manager.common.selectors import check_object_or_not_found
from mung_manager.tickets.containers import TicketContainer
from mung_manager.tickets.enums import TicketType


class TicketListAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="티켓 아이디")
        usage_time = serializers.IntegerField(label="사용 가능한 시간")
        usage_count = serializers.IntegerField(label="사용한 횟수")
        usage_period_in_days_count = serializers.IntegerField(label="사용 기간(일) 횟수")
        price = serializers.IntegerField(label="금액")
        ticket_type = serializers.CharField(label="티켓 타입")
        is_deleted = serializers.BooleanField(label="삭제 여부")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pet_kindergarden_selector = TicketContainer.pet_kindergarden_selector()
        self._ticket_selector = TicketContainer.ticket_selector()

    def get(self, request: Request, pet_kindergarden_id: int) -> Response:
        check_object_or_not_found(
            self._pet_kindergarden_selector.exists_by_id_and_user(
                pet_kindergarden_id=pet_kindergarden_id,
                user=request.user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        tickets = self._ticket_selector.get_queryset_by_pet_kindergarden_id(pet_kindergarden_id=pet_kindergarden_id)
        tickets_data = self.OutputSerializer(tickets, many=True).data
        return Response(data=tickets_data, status=status.HTTP_200_OK)


class TicketCreateAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        usage_time = serializers.IntegerField(
            required=False,
            min_value=0,
            default=0,
            label="사용 가능한 시간",
        )
        usage_count = serializers.IntegerField(required=True, min_value=1, label="사용 가능한 횟수")
        usage_period_in_days_count = serializers.IntegerField(required=True, min_value=1, label="사용 기간(일) 횟수")
        price = serializers.IntegerField(required=True, min_value=0, label="금액")
        ticket_type = serializers.ChoiceField(choices=[type.value for type in TicketType], label="티켓 타입")

    class OutputSerializer(BaseSerializer):
        id = serializers.IntegerField(label="티켓 아이디")
        usage_time = serializers.IntegerField(label="사용 가능한 시간")
        usage_count = serializers.IntegerField(label="사용 가능한 횟수")
        usage_period_in_days_count = serializers.IntegerField(label="사용 기간(일) 횟수")
        price = serializers.IntegerField(label="금액")
        ticket_type = serializers.CharField(label="티켓 타입")
        is_deleted = serializers.BooleanField(label="삭제 여부")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ticket_service = TicketContainer.ticket_service()

    def post(self, request: Request, pet_kindergarden_id: int) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        ticket = self._ticket_service.create_ticket(
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
            **input_serializer.validated_data,
        )
        ticket_data = self.OutputSerializer(ticket).data
        return Response(data=ticket_data, status=status.HTTP_201_CREATED)


class TicketDeleteView(APIAuthMixin, APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ticket_service = TicketContainer.ticket_service()

    def delete(self, request: Request, pet_kindergarden_id: int, ticket_id: int) -> Response:
        self._ticket_service.delete_ticket(
            ticket_id=ticket_id,
            pet_kindergarden_id=pet_kindergarden_id,
            user=request.user,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
