import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

pytestmark = pytest.mark.django_db


class TestJWTRefreshAPI:
    """
    JWTRefresh 테스트 클래스

    - Test List:
        Success:
            - jwt_refresh_api_success
        Fail:
            - jwt_refresh_api_fail_invalid_token
    """

    url = reverse("api-auth:jwt-refresh")

    def test_jwt_refresh_api_success(self, api_client, active_partner_user):
        """JWT Refresh POST 성공 테스트

        Args:
            api_client : API Client
            active_partner_user : 활성화된 사장님 유저
        """
        refresh = RefreshToken.for_user(active_partner_user)

        auth_data = {
            "refresh": str(refresh),
        }

        response = api_client.post(
            path=self.url,
            data=auth_data,
            format="json",
        )

        assert response.status_code == 200
        assert response.data["data"]["access_token"] is not None

    def test_jwt_refresh_api_fail_invalid_token(self, api_client):
        """JWT Refresh POST 실패 테스트 (유효하지 않은 토큰)

        Args:
            api_client : API Client
        """
        auth_data = {
            "refresh": "invalid_token",
        }

        response = api_client.post(
            path=self.url,
            data=auth_data,
            format="json",
        )

        assert response.status_code == 401
        assert response.data["code"] == "token_not_valid"
        assert response.data["message"] == "Token is invalid or expired"
