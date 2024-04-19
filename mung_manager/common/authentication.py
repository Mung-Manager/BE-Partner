from rest_framework_simplejwt.authentication import AuthUser, JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.utils import get_md5_hash_password

from mung_manager.common.exception.exceptions import (
    AuthenticationFailedException,
    InvalidTokenException,
)


class CustomJWTAuthentication(JWTAuthentication):
    """이 클래스는 JWTAuthentication을 상속받아 JWT 토큰을 검증하는 커스텀 클래스입니다.
    로그인 후의 모든 인증 관련 로직은 이 클래스에서 처리됩니다.
    """

    def get_user(self, validated_token: Token) -> AuthUser:
        """유효한 토큰을 검증하고 유저 객체를 반환합니다.

        Args:
            validated_token (Token): JWT Token 객체

        Returns:
            user (AuthUser): 유저 객체
        """
        # 토큰에서 user_id를 가져옵니다.
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidTokenException("Token contained no recognizable user identification")

        # user_id로 유저를 찾습니다.
        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailedException("User not found")

        # 유저가 활성화되어 있는지 확인합니다.
        if user.is_active is False:
            raise AuthenticationFailedException("User is inactive")

        # 토큰이 revoke되었는지 확인합니다.
        if api_settings.CHECK_REVOKE_TOKEN:
            if validated_token.get(api_settings.REVOKE_TOKEN_CLAIM) != get_md5_hash_password(user.password):
                raise AuthenticationFailedException("The user's password has been changed.")

        # 유저가 삭제되었는지 확인합니다.
        if user.is_deleted is True and user.deleted_at is not None:
            raise AuthenticationFailedException("User is deleted")

        return user

    def get_validated_token(self, raw_token: bytes) -> Token:
        """이 함수는 토큰을 검증합니다.

        Args:
            raw_token (bytes): 검증할 토큰
        Returns:
            Token: 검증된 토큰 객체
        """
        messages = []

        # 토큰을 검증합니다.
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError:
                messages.append(AuthToken.token_type)

        raise InvalidTokenException(f"{messages} Token is invalid or expired")
