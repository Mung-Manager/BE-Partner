from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from mung_manager.common.base.api_managers import BaseAPIManager
from mung_manager.schemas.errors.authentications import (
    ErrorAuthenticationPasswordChangedSchema,
    ErrorAuthenticationUserDeletedSchema,
    ErrorAuthenticationUserInactiveSchema,
    ErrorAuthenticationUserNotFoundSchema,
    ErrorAuthorizationHeaderSchema,
    ErrorTokenIdentificationSchema,
)
from mung_manager.schemas.errors.commons import (
    ErrorAuthenticationFailedSchema,
    ErrorInvalidParameterFormatSchema,
    ErrorInvalidTokenSchema,
    ErrorNotAuthenticatedSchema,
    ErrorPermissionDeniedSchema,
    ErrorUnknownServerSchema,
)
from mung_manager.schemas.errors.users import ErrorEmailAlreadyExistSchema
from mung_manager.users.apis.apis import UserProfileDetailAPI, UserProfileUpdateAPI


class UserProfileAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": UserProfileDetailAPI.as_view,
        "PATCH": UserProfileUpdateAPI.as_view,
    }

    @extend_schema(
        tags=["유저"],
        summary="유저 상세 조회",
        description="""
        Rogic
            - 유저 정보를 조회합니다.
        """,
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
            status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiTypes.OBJECT,
        },
        examples=[
            # 401
            ErrorAuthenticationFailedSchema,
            ErrorNotAuthenticatedSchema,
            ErrorInvalidTokenSchema,
            ErrorAuthorizationHeaderSchema,
            ErrorAuthenticationPasswordChangedSchema,
            ErrorAuthenticationUserDeletedSchema,
            ErrorAuthenticationUserInactiveSchema,
            ErrorAuthenticationUserNotFoundSchema,
            ErrorTokenIdentificationSchema,
            # 403
            ErrorPermissionDeniedSchema,
            # 500
            ErrorUnknownServerSchema,
        ],
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)

    @extend_schema(
        tags=["유저"],
        summary="유저 정보 수정",
        description="""
        Rogic
            - 유저가 자신의 정보를 수정합니다.
        """,
        request=VIEWS_BY_METHOD["PATCH"]().cls.InputSerializer,
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["PATCH"]().cls.OutputSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
            status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
            status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiTypes.OBJECT,
        },
        examples=[
            # 400
            ErrorInvalidParameterFormatSchema,
            ErrorEmailAlreadyExistSchema,
            # 401
            ErrorAuthenticationFailedSchema,
            ErrorNotAuthenticatedSchema,
            ErrorInvalidTokenSchema,
            ErrorAuthorizationHeaderSchema,
            ErrorAuthenticationPasswordChangedSchema,
            ErrorAuthenticationUserDeletedSchema,
            ErrorAuthenticationUserInactiveSchema,
            ErrorAuthenticationUserNotFoundSchema,
            ErrorTokenIdentificationSchema,
            # 403
            ErrorPermissionDeniedSchema,
            # 500
            ErrorUnknownServerSchema,
        ],
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        return self.VIEWS_BY_METHOD["PATCH"]()(request, *args, **kwargs)
