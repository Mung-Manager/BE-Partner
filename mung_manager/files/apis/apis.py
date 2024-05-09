from rest_framework import serializers, status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mung_manager.apis.mixins import APIAuthMixin
from mung_manager.common.base.serializers import BaseSerializer
from mung_manager.files.containers import FileContainer
from mung_manager.files.enums import FileResourceType


class FileUploadAPI(APIAuthMixin, APIView):
    parser_classes = (MultiPartParser,)

    class InputSerializer(BaseSerializer):
        file = serializers.FileField(help_text="업로드할 파일")
        resource_type = serializers.ChoiceField(
            choices=[e.value for e in FileResourceType],
            help_text="파일 리소스 타입",
        )

    class OutputSerializer(BaseSerializer):
        file_url = serializers.URLField(label="업로드된 파일 URL")

    def post(self, request: Request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        file_upload_service = FileContainer.file_upload_service(
            file_obj=input_serializer.validated_data["file"],
            resource_type=input_serializer.validated_data["resource_type"],
            user_id=request.user.id,
        )
        file_url = file_upload_service.upload_file()

        file_data = self.OutputSerializer({"file_url": file_url}).data
        return Response(file_data, status=status.HTTP_200_OK)
