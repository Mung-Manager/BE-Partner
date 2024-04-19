from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from mung_manager.common.base.api_managers import BaseAPIManager
from mung_manager.common.base.serializers import BaseResponseSerializer
from mung_manager.pet_kindergardens.apis.tickets.apis import (
    TicketCreateAPI,
    TicketDeleteView,
    TicketListAPI,
)


class TicketListAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "POST": TicketCreateAPI.as_view,
        "GET": TicketListAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원-이용권"],
        operation_summary="반려동물 유치원 티켓 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(
                data_serializer=VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["반려동물 유치원-이용권"],
        operation_summary="반려동물 유치원 티켓 생성",
        request_body=VIEWS_BY_METHOD["POST"]().cls.InputSerializer,
        responses={
            status.HTTP_201_CREATED: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["POST"]().cls.OutputSerializer),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["POST"]()(request, *args, **kwargs)


class TicketDetailManagerAPI(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "DELETE": TicketDeleteView.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원-이용권"],
        operation_summary="반려동물 유치원 티켓 삭제",
        responses={
            status.HTTP_204_NO_CONTENT: "",
        },
    )
    def delete(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["DELETE"]()(request, *args, **kwargs)
