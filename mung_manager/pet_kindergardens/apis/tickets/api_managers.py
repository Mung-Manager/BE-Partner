from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status

from mung_manager.common.base.api_managers import BaseAPIManager
from mung_manager.pet_kindergardens.apis.tickets.apis import (
    TicketCreateAPI,
    TicketDeleteView,
    TicketListAPI,
)
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
from mung_manager.schemas.errors.pet_kindergardens import (
    ErrorPetKindergardenNotFoundSchema,
)
from mung_manager.schemas.errors.tickets import ErrorTicketNotFoundSchema
from mung_manager.schemas.responses.commons import ResponseNoContentSchema


class TicketListAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "POST": TicketCreateAPI.as_view,
        "GET": TicketListAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원-이용권"],
        summary="반려동물 유치원 티켓 조회",
        description="""
        Rogic
            - 유저가 반려동물 유치원 티켓을 조회합니다.
        """,
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
            status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
            status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT,
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
            # 404
            ErrorPetKindergardenNotFoundSchema,
            # 500
            ErrorUnknownServerSchema,
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)

    @extend_schema(
        tags=["반려동물 유치원-이용권"],
        summary="반려동물 유치원 티켓 생성",
        description="""
        Rogic
            - 유저가 반려동물 유치원 티켓을 생성합니다.
        """,
        request=VIEWS_BY_METHOD["POST"]().cls.InputSerializer,
        responses={
            status.HTTP_201_CREATED: VIEWS_BY_METHOD["POST"]().cls.OutputSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
            status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
            status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiTypes.OBJECT,
        },
        examples=[
            # 400
            ErrorInvalidParameterFormatSchema,
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
            # 404
            ErrorPetKindergardenNotFoundSchema,
            # 500
            ErrorUnknownServerSchema,
        ],
    )
    def post(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["POST"]()(request, *args, **kwargs)


class TicketDetailManagerAPI(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "DELETE": TicketDeleteView.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원-이용권"],
        summary="반려동물 유치원 티켓 삭제",
        description="""
        Rogic
            - 유저가 반려동물 유치원 티켓을 삭제합니다.
        """,
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiTypes.OBJECT,
            status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
            status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
            status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiTypes.OBJECT,
        },
        examples=[
            # 204
            ResponseNoContentSchema,
            # 400
            ErrorInvalidParameterFormatSchema,
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
            # 404
            ErrorPetKindergardenNotFoundSchema,
            ErrorTicketNotFoundSchema,
            # 500
            ErrorUnknownServerSchema,
        ],
    )
    def delete(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["DELETE"]()(request, *args, **kwargs)
