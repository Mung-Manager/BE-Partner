from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from mung_manager.common.base.api_managers import BaseAPIManager
from mung_manager.files.apis.apis import FileUploadAPI
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
from mung_manager.schemas.errors.files import (
    ErrorFildUploadFailedSchema,
    ErrorFileMaxSizeExceededSchema,
    ErrorImageInvalidSchema,
)


class FileUploadAPIManager(BaseAPIManager):
    parser_classes = (MultiPartParser,)

    VIEWS_BY_METHOD = {
        "POST": FileUploadAPI.as_view,
    }

    @extend_schema(
        tags=["파일"],
        summary="파일 업로드",
        description="""
        Rogic
            - 유저가 AWS S3에 파일을 업로드합니다. (최대 10MB)
        """,
        request=VIEWS_BY_METHOD["POST"]().cls.InputSerializer,
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["POST"]().cls.OutputSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
            status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
            status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiTypes.OBJECT,
        },
        examples=[
            # 400
            ErrorInvalidParameterFormatSchema,
            ErrorFildUploadFailedSchema,
            ErrorFileMaxSizeExceededSchema,
            ErrorImageInvalidSchema,
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
    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.VIEWS_BY_METHOD["POST"]()(request, *args, **kwargs)
