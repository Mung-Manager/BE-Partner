from mung_manager.authentication.services.auth import AuthService


class TestGenerateToken:
    """
    AuthService의 generate_token 테스트 클래스

    - Test List:
        Success:
            - generate_token_success
    """

    def setup_method(self):
        self.auth_service = AuthService()

    def test_generate_token_success(self, active_partner_user):
        """토큰 생성 성공 테스트

        Args:
            active_partner_user : 활성화된 사장님 유저
        """
        refresh_token, access_token = self.auth_service.generate_token(active_partner_user)

        assert refresh_token is not None
        assert access_token is not None
