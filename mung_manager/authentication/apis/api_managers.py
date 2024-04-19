from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from mung_manager.authentication.apis.apis import JWTRefreshAPI, KakaoLoginAPI
from mung_manager.common.base.api_managers import BaseAPIManager
from mung_manager.common.base.serializers import BaseResponseSerializer


class JWTRefreshAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "POST": JWTRefreshAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="인증 토큰 재발급",
        operation_description="refresh token을 입력받아 access token을 재발급합니다.",
        request_body=TokenRefreshSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["POST"]().cls.OutputSerializer),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["POST"]()(request, *args, **kwargs)


class KakaoLoginAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": KakaoLoginAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["인증"],
        operation_summary="카카오 로그인 콜백",
        operation_description="""
        카카오 로그인 콜백 API 입니다. 카카오 로그인을 완료하면, 카카오에서 전달받은 정보를 토대로
        앱 유저를 생성하고, 액세스 토큰과 리프레쉬 토큰을 발급합니다.
        """,
        query_serializer=VIEWS_BY_METHOD["GET"]().cls.InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(
                data_serializer=VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)
