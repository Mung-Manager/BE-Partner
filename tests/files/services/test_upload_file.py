import tempfile

import pytest
from django.test import override_settings
from partner_service.mung_manager.files.services.files import FileUploadService
from PIL import Image

from mung_manager.common.exception.exceptions import ValidationException


class TestUploadFile:
    """
    FileUploadService의 upload_file 메서드의 테스트 클래스

    - Test List:
        Success:
            - test_upload_file_success
        Fail:
            - test_upload_file_fail_invalid_file_type
            - test_upload_file_fail_invalid_file_size

    """

    def get_temporary_image(self):
        """임시 이미지 파일을 생성합니다."""
        size = (100, 100)
        color = (255, 0, 0, 0)
        image = Image.new("RGBA", size, color)
        temp_file = tempfile.NamedTemporaryFile(suffix=".png")
        image.save(temp_file, "png")
        return temp_file

    def setup_method(self):
        self.temp_file = self.get_temporary_image()

    def test_upload_file_success(self, mocker):
        """파일 업로드 성공 테스트

        Args:
            mocker : mocker 객체
        """
        mocker.patch("django.core.files.storage.default_storage.save")

        service = FileUploadService(
            file_obj=self.temp_file,
            resource_type="pet_kindergarden",
            user_id=1,
        )
        upload_path = service.upload_file()
        assert upload_path is not None

    def test_upload_file_fail_invalid_file_type(self, mocker):
        """파일 업로드 실패 테스트 (잘못된 파일 타입)

        Args:
            mocker : mocker 객체
        """
        mocker.patch("django.core.files.storage.default_storage.save")

        temp_file = tempfile.NamedTemporaryFile(suffix=".txt")

        service = FileUploadService(
            file_obj=temp_file,
            resource_type="pet_kindergarden",
            user_id=1,
        )
        with pytest.raises(ValidationException) as e:
            service.upload_file()

        assert isinstance(e.value, ValidationException)

    @override_settings(FILE_MAX_SIZE=-1)
    def test_upload_file_fail_invalid_file_size(self, mocker):
        """파일 업로드 실패 테스트 (잘못된 파일 크기)

        Args:
            mocker : mocker 객체
        """
        mocker.patch("django.core.files.storage.default_storage.save")

        service = FileUploadService(
            file_obj=self.temp_file,
            resource_type="pet_kindergarden",
            user_id=1,
        )
        with pytest.raises(ValidationException) as e:
            service.upload_file()

        assert isinstance(e.value, ValidationException)
