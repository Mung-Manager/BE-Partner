from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from mung_manager.common.base.api_managers import BaseAPIManager
from mung_manager.common.base.serializers import BaseResponseSerializer
from mung_manager.pet_kindergardens.apis.pet_kindergardens.apis import (
    PetKindergardenCreateAPI,
    PetKindergardenProfileAPI,
    PetKindergardenSearchAPI,
)


class PetkindergardenListAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "POST": PetKindergardenCreateAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원"],
        operation_summary="반려동물 유치원 생성",
        request_body=VIEWS_BY_METHOD["POST"]().cls.InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["POST"]().cls.OutputSerializer),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["POST"]()(request, *args, **kwargs)


class PetkindergardenSearchAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": PetKindergardenSearchAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원"],
        operation_summary="네이버 데이터 반려동물 유치원 검색",
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


class PetkindergardenProfileAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": PetKindergardenProfileAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["반려동물 유치원"],
        operation_summary="반려동물 유치원 프로필 조회",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(
                data_serializer=VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)
