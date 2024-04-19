from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mung_manager.common.base.serializers import BaseSerializer
from mung_manager.common.mixins import APIAuthMixin
from mung_manager.common.response import create_response
from mung_manager.files.containers import FileContainer
from mung_manager.files.enums import FileResourceType


class FileUploadAPI(APIAuthMixin, APIView):
    parser_classes = (MultiPartParser,)

    class InputSerializer(BaseSerializer):
        file = serializers.FileField()
        resource_type = serializers.ChoiceField(choices=[e.value for e in FileResourceType])

    class OutputSerializer(BaseSerializer):
        file_url = serializers.URLField()

    def post(self, request: Request) -> Response:
        """유저가 AWS S3에 파일을 업로드합니다. (최대 10MB)
        url: /partner/api/v1/files/upload

        Args:
            file (File): 업로드할 파일
            resource_type (str): 파일의 리소스 타입

        Returns:
            OutputSerializer:
                file_url: 업로드된 파일의 URL

        Raises:
            400: 파일이 10MB를 초과하는 경우, 파일이 이미지가 아닌 경우, 그외 파일 업로드 실패한 경우
            401: 유저를 없거나, 활성화 상태가 아니거나, 탈퇴한 경우
            403: 사장님이 아닌 경우
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        file_upload_service = FileContainer.file_upload_service(
            file_obj=input_serializer.validated_data["file"],
            resource_type=input_serializer.validated_data["resource_type"],
            user_id=request.user.id,
        )
        file_url = file_upload_service.upload_file()

        file_data = self.OutputSerializer({"file_url": file_url}).data
        return create_response(file_data, status_code=status.HTTP_200_OK)
