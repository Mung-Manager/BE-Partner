import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestKakaoLoginAPI:
    """
    KakaoLogin 테스트 클래스

    - Test List:
        Success:
            - kakao_login_api_success
            - @TODO: kakao_login_api_success_partner_enrolled
        Fail:
            - kakao_login_api_fail_missing_code
            - kakao_login_api_fail_missing_redirect_uri
            - kakao_login_api_fail_exist_error
    """

    url = reverse("api-auth:kakao-login-callback")

    def test_kakao_login_api_success(self, api_client, mocker, user_social_provider, group):
        """카카오 로그인 성공 테스트

        Args:
            api_client : API Client
            mocker : mocker 객체
            user_social_provider : 유저 제공자
            group : 권한 그룹
        """
        user_info_response = {
            "id": 123456789,
            "kakao_account": {
                "email": "test@test.com",
                "name": "test",
                "phone_number": "+82 10-1234-1234",
                "birthyear": "2000",
                "birthday": "0101",
                "gender": "male",
            },
        }

        mocker.patch("mung_manager.authentication.services.kakao_oauth.KakaoLoginFlowService.get_token", return_value=mocker.Mock())
        mocker.patch(
            "mung_manager.authentication.services.kakao_oauth.KakaoLoginFlowService.get_user_info", return_value=user_info_response
        )

        response = api_client.get(
            path=self.url,
            data={"code": "code", "redirect_uri": "http://localhost:8000"},
        )

        assert response.status_code == 200
        assert response.data["data"]["access_token"] is not None
        assert response.data["data"]["refresh_token"] is not None
        assert response.data["data"]["is_partner_enrolled"] is False

    # def test_kakao_login_api_fail_missing_code(self, api_client):
    #     """카카오 로그인 실패 테스트 (코드가 누락된 경우)

    #     Args:
    #         api_client : API Client
    #     """
    #     response = api_client.get(path=self.url)

    #     assert response.status_code == 401
    #     assert response.data["code"] == "authentication_failed"
    #     assert response.data["message"] == "Code is not provided"

    # def test_kakao_login_api_fail_missing_redirect_uri(self, api_client):
    #     """카카오 로그인 실패 테스트 (리다이렉트 URI가 누락된 경우)

    #     Args:
    #         api_client : API Client
    #     """
    #     response = api_client.get(
    #         path=self.url,
    #         data={
    #             "code": "code",
    #         },
    #     )

    #     assert response.status_code == 401
    #     assert response.data["code"] == "authentication_failed"
    #     assert response.data["message"] == "Redirect URI is not provided"

    # def test_kakao_login_api_fail_exist_error(self, api_client):
    #     """카카오 로그인 실패 테스트 (에러가 발생한 경우)

    #     Args:
    #         api_client : API Client
    #     """
    #     response = api_client.get(
    #         path=self.url,
    #         data={
    #             "error": "error",
    #         },
    #     )

    #     assert response.status_code == 401
    #     assert response.data["code"] == "authentication_failed"
    #     assert response.data["message"] == "error"
