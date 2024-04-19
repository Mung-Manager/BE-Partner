from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from mung_manager.common.base.api_managers import BaseAPIManager
from mung_manager.common.base.serializers import BaseResponseSerializer
from mung_manager.pet_kindergardens.apis.customers.apis import (
    CustomerBatchRegisterAPI,
    CustomerCreateAPI,
    CustomerDetailAPI,
    CustomerListAPI,
    CustomerPetDeleteAPI,
    CustomerTicketActiveListAPI,
    CustomerTicketCreateAPI,
    CustomerTicketListAPI,
    CustomerTicketLogListAPI,
    CustomerToggleActiveAPI,
    CustomerUpdateAPI,
)


class CustomerListAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "POST": CustomerCreateAPI.as_view,
        "GET": CustomerListAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원-고객"],
        operation_summary="반려동물 유치원 고객 목록 조회",
        query_serializer=VIEWS_BY_METHOD["GET"]().cls.FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(
                data_serializer=VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
                pagination_serializer=True,
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["반려동물 유치원-고객"],
        operation_summary="반려동물 유치원 고객 등록",
        request_body=VIEWS_BY_METHOD["POST"]().cls.InputSerializer,
        responses={status.HTTP_201_CREATED: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["POST"]().cls.OutputSerializer)},
    )
    def post(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["POST"]()(request, *args, **kwargs)


class CustomerBatchRegisterAPIManager(BaseAPIManager):
    parser_classes = (MultiPartParser,)

    VIEWS_BY_METHOD = {
        "POST": CustomerBatchRegisterAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원-고객"],
        operation_summary="반려동물 유치원 고객 일괄 등록",
        request_body=VIEWS_BY_METHOD["POST"]().cls.InputSerializer,
        responses={
            status.HTTP_201_CREATED: BaseResponseSerializer(
                data_serializer=VIEWS_BY_METHOD["POST"]().cls.OutputSerializer,
                data_serializer_many=True,
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["POST"]()(request, *args, **kwargs)


class CustomerDetailAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": CustomerDetailAPI.as_view,
        "PUT": CustomerUpdateAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원-고객"],
        operation_summary="반려동물 유치원 고객 상세 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["GET"]().cls.OutputSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["반려동물 유치원-고객"],
        operation_summary="반려동물 유치원 고객 수정",
        request_body=VIEWS_BY_METHOD["PUT"]().cls.InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["PUT"]().cls.OutputSerializer),
        },
    )
    def put(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["PUT"]()(request, *args, **kwargs)


class CustomerToggleActiveAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "PATCH": CustomerToggleActiveAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원-고객"],
        operation_summary="반려동물 유치원 고객 활성화/비활성화",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["PATCH"]().cls.OutputSerializer),
        },
    )
    def patch(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["PATCH"]()(request, *args, **kwargs)


class CustomerTicketActiveListAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": CustomerTicketActiveListAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원-고객"],
        operation_summary="반려동물 유치원 고객 티켓 목록 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(
                data_serializer=VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
                data_serializer_many=True,
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)


class CustomerTicketListAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": CustomerTicketListAPI.as_view,
        "POST": CustomerTicketCreateAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원-고객"],
        operation_summary="반려동물 고객 정보 이용권 등록 목록 조회",
        query_serializer=VIEWS_BY_METHOD["GET"]().cls.FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(
                data_serializer=VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
                pagination_serializer=True,
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["반려동물 유치원-고객"],
        operation_summary="반려동물 고객 정보 이용권 등록",
        request_body=VIEWS_BY_METHOD["POST"]().cls.InputSerializer,
        responses={
            status.HTTP_201_CREATED: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["POST"]().cls.OutputSerializer),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["POST"]()(request, *args, **kwargs)


class CustomerTicketLogListAPIManger(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": CustomerTicketLogListAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원-고객"],
        operation_summary="반려동물 고객 이용권 사용 내역 목록 조회",
        query_serializer=VIEWS_BY_METHOD["GET"]().cls.FilterSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(
                data_serializer=VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
                pagination_serializer=True,
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)


class CustomerPetDetailAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "DELETE": CustomerPetDeleteAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원-고객"],
        operation_summary="반려동물 유치원 고객 반려동물 삭제 여부 확인",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["DELETE"]().cls.OutputSerializer),
        },
    )
    def delete(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["DELETE"]()(request, *args, **kwargs)
