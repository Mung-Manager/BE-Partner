import pytest

from mung_manager.authentication.services.kakao_oauth import (
    KakaoAccessToken,
    KakaoLoginFlowService,
)
from mung_manager.common.exception.exceptions import AuthenticationFailedException


class TestKakaoLoginFlowService:
    """
    KakaoLoginFlowService의 테스트 클래스

    - Test List:
        Success:
            - get_token_success
            - get_user_info_success
        Fail:
            - get_token_fail
            - get_user_info_fail
    """

    def setup_method(self):
        self.service = KakaoLoginFlowService()

    def test_get_token_success(self, mocker):
        """카카오 로그인 토큰 발급 성공 테스트

        Args:
            mocker : mocker 객체
        """
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "test_access_token"}

        mocker.patch("mung_manager.authentication.services.kakao_oauth.requests.post", return_value=mock_response)

        token = self.service.get_token(code="test_code", redirect_uri="http://localhost:8000")
        assert token.access_token == "test_access_token"

    def test_get_user_info_success(self, mocker):
        """카카오 유저 정보 조회 성공 테스트

        Args:
            mocker : mocker 객체
        """
        mock_response = mocker.Mock()
        mock_response.status_code = 200
        mock_response.text = """
        {
            "id": 123456789,
            "kakao_account": {
                "name": "멍매니저",
                "email": "mung_manager@test.com",
                "phone_number": "+82 10-1234-1234",
                "birthyear": "2000",
                "birthday": "0101",
                "gender": "male"
            }
        }
        """
        mocker.patch("mung_manager.authentication.services.kakao_oauth.requests.get", return_value=mock_response)
        kakao_token = KakaoAccessToken(access_token="test_access_token")
        user_info = self.service.get_user_info(kakao_token)

        assert user_info["id"] == 123456789
        assert user_info["kakao_account"]["name"] == "멍매니저"
        assert user_info["kakao_account"]["email"] == "mung_manager@test.com"
        assert user_info["kakao_account"]["phone_number"] == "+82 10-1234-1234"
        assert user_info["kakao_account"]["birthyear"] == "2000"
        assert user_info["kakao_account"]["birthday"] == "0101"
        assert user_info["kakao_account"]["gender"] == "male"

    def test_get_token_fail(self, mocker):
        """카카오 로그인 토큰 발급 실패 테스트

        Args:
            mocker : mocker 객체
        """
        mock_response = mocker.Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"access_token": "test_access_token"}

        mocker.patch("mung_manager.authentication.services.kakao_oauth.requests.post", return_value=mock_response)

        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_token(code="test_code", redirect_uri="http://localhost:8000")

        assert e.value.detail == "Failed to get access token from Kakao."
        assert e.value.status_code == 401

    def test_get_user_info_fail(self, mocker):
        """카카오 유저 정보 조회 실패 테스트

        Args:
            mocker : mocker 객체
        """
        mock_response = mocker.Mock()
        mock_response.status_code = 401

        mocker.patch("mung_manager.authentication.services.kakao_oauth.requests.get", return_value=mock_response)
        kakao_token = KakaoAccessToken(access_token="test_access_token")
        with pytest.raises(AuthenticationFailedException) as e:
            self.service.get_user_info(kakao_token)

        assert e.value.detail == "Failed to get user info from Kakao."
        assert e.value.status_code == 401
