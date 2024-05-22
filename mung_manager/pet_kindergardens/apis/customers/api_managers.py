from djangorestframework_camel_case.parser import CamelCaseMultiPartParser
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import status

from mung_manager.common.base.api_managers import BaseAPIManager
from mung_manager.pet_kindergardens.apis.customers.apis import (
    CustomerBatchRegisterAPI,
    CustomerCreateAPI,
    CustomerDetailAPI,
    CustomerListAPI,
    CustomerTicketActiveListAPI,
    CustomerTicketCreateAPI,
    CustomerTicketListAPI,
    CustomerTicketLogListAPI,
    CustomerToggleActiveAPI,
    CustomerUpdateAPI,
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
    ErrorPhoneNumberInvalidSchema,
    ErrorUnknownServerSchema,
)
from mung_manager.schemas.errors.customers import (
    ErrorCustomerAlreadyExistsSchema,
    ErrorCustomerCsvPhoneNumberDuplicatedSchema,
    ErrorCustomerNotFoundSchema,
    ErrorCustomerPetAlreadyExistsSchema,
    ErrorCustomerPetNameDuplicatedSchema,
)
from mung_manager.schemas.errors.pet_kindergardens import (
    ErrorPetKindergardenNotFoundSchema,
)
from mung_manager.schemas.errors.tickets import ErrorTicketNotFoundSchema


class CustomerListAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "POST": CustomerCreateAPI.as_view,
        "GET": CustomerListAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원-고객"],
        summary="반려동물 유치원 고객 목록 조회",
        description="""
        Rogic
            - 유저가 반려동물 유치원 고객 목록을 조회합니다.
        """,
        parameters=[VIEWS_BY_METHOD["GET"]().cls.FilterSerializer],
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["GET"]().cls.OutputSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
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
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)

    @extend_schema(
        tags=["반려동물 유치원-고객"],
        summary="반려동물 유치원 고객 등록",
        description="""
        Rogic
            - 유저가 반려동물 유치원 고객을 등록합니다.
        """,
        request=VIEWS_BY_METHOD["POST"]().cls.InputSerializer,
        responses={
            status.HTTP_201_CREATED: VIEWS_BY_METHOD["POST"]().cls.OutputSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
            status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
            status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
            status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiTypes.OBJECT,
        },
        examples=[
            # 400
            ErrorInvalidParameterFormatSchema,
            ErrorCustomerAlreadyExistsSchema,
            ErrorPhoneNumberInvalidSchema,
            ErrorCustomerPetNameDuplicatedSchema,
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


class CustomerBatchRegisterAPIManager(BaseAPIManager):
    parser_classes = [CamelCaseMultiPartParser]

    VIEWS_BY_METHOD = {
        "POST": CustomerBatchRegisterAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원-고객"],
        summary="반려동물 유치원 고객 일괄 등록",
        description="""
        Rogic
            - 유저가 반려동물 유치원 고객을 일괄 등록합니다.
        """,
        request=VIEWS_BY_METHOD["POST"]().cls.InputSerializer,
        responses={
            status.HTTP_201_CREATED: VIEWS_BY_METHOD["POST"]().cls.OutputSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
            status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
            status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
            status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiTypes.OBJECT,
        },
        examples=[
            # 400
            ErrorInvalidParameterFormatSchema,
            ErrorCustomerCsvPhoneNumberDuplicatedSchema,
            ErrorCustomerPetNameDuplicatedSchema,
            ErrorPhoneNumberInvalidSchema,
            ErrorCustomerAlreadyExistsSchema,
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


class CustomerDetailAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": CustomerDetailAPI.as_view,
        "PUT": CustomerUpdateAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원-고객"],
        summary="반려동물 유치원 고객 상세 조회",
        description="""
        Rogic
            - 유저가 반려동물 유치원 고객 상세 정보를 조회합니다.
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
            ErrorCustomerNotFoundSchema,
            ErrorPetKindergardenNotFoundSchema,
            # 500
            ErrorUnknownServerSchema,
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)

    @extend_schema(
        tags=["반려동물 유치원-고객"],
        summary="반려동물 유치원 고객 수정",
        description="""
        Rogic
            - 유저가 반려동물 유치원 고객 정보를 수정합니다.
        """,
        request=VIEWS_BY_METHOD["PUT"]().cls.InputSerializer,
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["PUT"]().cls.OutputSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
            status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
            status.HTTP_403_FORBIDDEN: OpenApiTypes.OBJECT,
            status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT,
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiTypes.OBJECT,
        },
        examples=[
            # 400
            ErrorInvalidParameterFormatSchema,
            ErrorCustomerPetNameDuplicatedSchema,
            ErrorPhoneNumberInvalidSchema,
            ErrorCustomerPetAlreadyExistsSchema,
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
            ErrorCustomerNotFoundSchema,
            ErrorPetKindergardenNotFoundSchema,
            # 500
            ErrorUnknownServerSchema,
        ],
    )
    def put(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["PUT"]()(request, *args, **kwargs)


class CustomerToggleActiveAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "PATCH": CustomerToggleActiveAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원-고객"],
        summary="반려동물 유치원 고객 활성화/비활성화",
        description="""
        Rogic
            - 유저가 반려동물 유치원 고객을 활성화/비활성화합니다.
        """,
        responses={
            status.HTTP_200_OK: VIEWS_BY_METHOD["PATCH"]().cls.OutputSerializer,
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
            ErrorCustomerNotFoundSchema,
            ErrorPetKindergardenNotFoundSchema,
            # 500
            ErrorUnknownServerSchema,
        ],
    )
    def patch(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["PATCH"]()(request, *args, **kwargs)


class CustomerTicketActiveListAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": CustomerTicketActiveListAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원-고객"],
        summary="반려동물 유치원 고객 티켓 목록 조회",
        description="""
        Rogic
            - 유저가 반려동물 유치원 고객 티켓 목록을 조회합니다.
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


class CustomerTicketListAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": CustomerTicketListAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원-고객"],
        summary="반려동물 고객 정보 이용권 등록 목록 조회",
        description="""
        Rogic
            - 유저가 반려동물 유치원 고객 정보 이용권 등록 목록을 조회합니다.
        """,
        parameters=[VIEWS_BY_METHOD["GET"]().cls.FilterSerializer],
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
            ErrorCustomerNotFoundSchema,
            # 500
            ErrorUnknownServerSchema,
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)


class CustomerTicketDetailAPIManager(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "POST": CustomerTicketCreateAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원-고객"],
        summary="반려동물 고객 정보 이용권 등록",
        description="""
        Rogic
            - 유저가 반려동물 유치원 고객 정보 이용권을 등록합니다.
        """,
        responses={
            status.HTTP_201_CREATED: VIEWS_BY_METHOD["POST"]().cls.OutputSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
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
            ErrorCustomerNotFoundSchema,
            ErrorTicketNotFoundSchema,
            # 500
            ErrorUnknownServerSchema,
        ],
    )
    def post(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["POST"]()(request, *args, **kwargs)


class CustomerTicketLogListAPIManger(BaseAPIManager):
    VIEWS_BY_METHOD = {
        "GET": CustomerTicketLogListAPI.as_view,
    }

    @extend_schema(
        tags=["반려동물 유치원-고객"],
        summary="반려동물 고객 이용권 사용 내역 목록 조회",
        description="""
        Rogic
            - 유저가 반려동물 유치원 고객 이용권 사용 내역 목록을 조회합니다.
        """,
        parameters=[VIEWS_BY_METHOD["GET"]().cls.FilterSerializer],
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
            ErrorCustomerNotFoundSchema,
            # 500
            ErrorUnknownServerSchema,
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["GET"]()(request, *args, **kwargs)
