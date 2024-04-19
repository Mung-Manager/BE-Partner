from datetime import datetime

from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from mung_manager.authentication.containers import AuthenticationContainer
from mung_manager.common.base.serializers import BaseSerializer
from mung_manager.common.exception.exceptions import (
    AuthenticationFailedException,
    InvalidTokenException,
)
from mung_manager.common.response import create_response
from mung_manager.pet_kindergardens.containers import PetKindergardenContainer
from mung_manager.users.containers import UserContainer
from mung_manager.users.enums import UserProvider


class JWTRefreshAPI(TokenRefreshView):
    class OutputSerializer(BaseSerializer):
        access_token = serializers.CharField()

    def post(self, request: Request) -> Response:
        """refresh token을 입력받아 access token을 발급합니다.
        url: /partner/api/v1/auth/jwt/refresh

        Args:
            refresh (str): 리프레쉬 토큰

        Returns:
            OutputSerializer: 인증 토큰 정보
                access_token (str): 액세스 토큰

        Raises:
            401: 토큰이 유효하지 않거나 만료된 경우
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            raise InvalidTokenException("Token is invalid or expired")

        token_data = self.OutputSerializer({"access_token": serializer.validated_data["access"]}).data
        return create_response(data=token_data, status_code=status.HTTP_200_OK)


class KakaoLoginAPI(APIView):
    class InputSerializer(BaseSerializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)
        redirect_uri = serializers.CharField(required=False)

    class OutputSerializer(BaseSerializer):
        access_token = serializers.CharField()
        refresh_token = serializers.CharField()
        is_partner_enrolled = serializers.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._auth_service = AuthenticationContainer.auth_service()
        self._kakao_login_flow_service = AuthenticationContainer.kakao_login_flow_service()
        self._user_service = UserContainer.user_service()
        self._pet_kindergarden_selector = PetKindergardenContainer.pet_kindergarden_selector()

    def get(self, request: Request) -> Response:
        """카카오 로그인 콜백 API 입니다. 카카오 로그인을 완료하면, 카카오에서 전달받은 정보를 토대로
            앱 유저를 생성하고, 액세스 토큰과 리프레쉬 토큰을 발급합니다.
        url: /partner/api/v1/auth/kakao/callback

        Args:
            InputSerializer: 카카오 로그인 콜백 데이터
                code (str): 카카오 인증 코드
                error (str): 카카오 에러 코드
                redirect_uri (str): 카카오 리다이렉트 URI

        Returns:
            OutputSerializer: 인증 토큰 정보
                access_token (str): 액세스 토큰
                refresh_token (str): 리프레쉬 토큰
                is_partner_enrolled (bool): 반려견 유치원 등록 여부

        Raises:
            400: 카카오 인증 코드가 없는 경우, 리다이렉트 URI가 없는 경우, 카카오 에러 코드가 있는 경우
            401: 카카오 전화번호 인증이 되어있지 않은 경우, 그외 카카오 로그인 실패한 경우
        """
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data
        code = validated_data.get("code")
        error = validated_data.get("error")
        redirect_uri = validated_data.get("redirect_uri")

        if error is not None:
            raise AuthenticationFailedException(error)

        if code is None:
            raise AuthenticationFailedException("Code is not provided")

        if redirect_uri is None:
            raise AuthenticationFailedException("Redirect URI is not provided")

        # 카카오 로그인 플로우
        kakao_token = self._kakao_login_flow_service.get_token(code=code, redirect_uri=redirect_uri)
        user_info = self._kakao_login_flow_service.get_user_info(kakao_token=kakao_token)

        # 유저 정보 추출
        social_id = user_info["id"]
        email = user_info["kakao_account"]["email"]
        name = user_info["kakao_account"]["name"]
        phone_number = user_info["kakao_account"].get("phone_number")
        birthyear = user_info["kakao_account"].get("birthyear")
        birthday = user_info["kakao_account"].get("birthday")
        gender = user_info["kakao_account"].get("gender")
        has_phone_number = user_info["kakao_account"].get("has_phone_number")

        # 카카오 전화번호 인증 여부 확인
        if has_phone_number is False:
            raise AuthenticationFailedException("Kakao phone number is not authenticated.")

        phone_number = phone_number.replace("+82 ", "0")
        birth = datetime.strptime(birthyear + birthday, "%Y%m%d") if birthyear and birthday else ""
        gender = "F" if gender == "female" else "M" if gender == "male" else ""

        # 소셜 유저 생성
        user = self._user_service.create_social_user(
            social_id=social_id,
            name=name,
            email=email,
            phone_number=phone_number,
            birth=birth,
            gender=gender,
            social_provider=UserProvider.KAKAO.value,
        )

        # 반려견 유치원 등록 여부 확인
        is_partner_enrolled = self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_user(user=user)

        # 유저 토큰 발급
        self._auth_service.authenticate_user(user)
        refresh_token, access_token = self._auth_service.generate_token(user)
        auth_data = self.OutputSerializer(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "is_partner_enrolled": is_partner_enrolled,
            }
        ).data
        return create_response(data=auth_data, status_code=status.HTTP_200_OK)
