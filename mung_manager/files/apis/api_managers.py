from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from mung_manager.common.base.api_managers import BaseAPIManager
from mung_manager.common.base.serializers import BaseResponseSerializer
from mung_manager.files.apis.apis import FileUploadAPI


class FileUploadAPIManager(BaseAPIManager):
    parser_classes = (MultiPartParser,)

    VIEWS_BY_METHOD = {
        "POST": FileUploadAPI.as_view,
    }

    @swagger_auto_schema(
        tags=["파일"],
        operation_summary="파일 업로드",
        operation_description="유저가 AWS S3에 파일을 업로드합니다. (최대 10MB)",
        request_body=VIEWS_BY_METHOD["POST"]().cls.InputSerializer,
        responses={
            status.HTTP_200_OK: BaseResponseSerializer(data_serializer=VIEWS_BY_METHOD["POST"]().cls.OutputSerializer),
        },
    )
    def post(self, request, *args, **kwargs):
        return self.VIEWS_BY_METHOD["POST"]()(request, *args, **kwargs)
