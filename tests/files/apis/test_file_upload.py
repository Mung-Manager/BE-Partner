import tempfile

import pytest
from django.urls import reverse
from PIL import Image

from tests.utils import IsAuthenticateTestCase

pytestmark = pytest.mark.django_db


class TestFileUploadAPI(IsAuthenticateTestCase):
    """
    FileUploadAPI 테스트 클래스

    - Test List:
        Success:
            - file_upload_success
        Fail:
            - file_upload_fail_not_authenticated
            - file_upload_fail_permission_denied
    """

    url = reverse("api-files:file-upload")

    def test_file_upload_success(self, mocker, active_partner_user):
        """파일 업로드 성공 테스트

        Args:
            mocker : mocker 객체
        """
        access_token = self.obtain_token(active_partner_user)
        self.authenticate_with_token(access_token)

        mocker.patch("django.core.files.storage.default_storage.save")

        image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        Image.new("RGB", (100, 100)).save(image)

        with open(image, "rb") as file:
            response = self.client.post(self.url, {"file": file, "resource_type": "pet_kindergarden"})

        assert response.status_code == 200
        assert response.data["data"]["file_url"] is not None

    def test_file_upload_fail_not_authenticated(self):
        """파일 업로드 실패 테스트 (인증되지 않은 사용자)"""
        response = self.client.post(self.url)

        assert response.status_code == 401
        assert response.data["code"] == "not_authenticated"
        assert response.data["message"] == "Authentication credentials were not provided."

    def test_file_upload_fail_permission_denied(self, active_guest_user):
        """파일 업로드 실패 테스트 (권한 없는 사용자)

        Args:
            active_guest_user : 활성화된 손님 유저
        """
        access_token = self.obtain_token(active_guest_user)
        self.authenticate_with_token(access_token)
        response = self.client.post(self.url)

        assert response.status_code == 403
        assert response.data["code"] == "permission_denied"
        assert response.data["message"] == "You do not have permission to perform this action."
