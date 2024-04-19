from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from mung_manager.common.base.api_managers import BaseAPIManager
from mung_manager.common.base.serializers import BaseResponseSerializer
from mung_manager.users.apis.apis import UserProfileDetailAPI, UserProfileUpdateAPI


class UserProfileAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": UserProfileDetailAPI.as_view,
        "PATCH": UserProfileUpdateAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 상세 조회",
        operation_description="유저가 자신의 정보를 상세 조회합니다.",
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["GET"]().cls.OutputSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["유저"],
        operation_summary="유저 정보 수정",
        operation_description="유저가 자신의 정보를 수정합니다.",
        request_body=VIEWS_BY_METHOD["PATCH"]().cls.InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["PATCH"]().cls.OutputSerializer),
        },
    )
    def patch(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["PATCH"]()(request, *args, **kwargs)
