from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mung_manager.common.base.serializers import BaseSerializer
from mung_manager.common.mixins import APIAuthMixin
from mung_manager.common.response import create_response
from mung_manager.users.containers import UserContainer


class UserProfileDetailAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        name = serializers.CharField()
        email = serializers.EmailField()
        phone_number = serializers.CharField()

    def get(self, request: Request) -> Response:
        """유저가 자신의 정보를 상세 조회합니다.
        url: /partner/api/v1/users/profile

        Returns:
            OutSerializer: 유저 정보
                name (str): 이름
                email (str): 이메일
                phone_number (str): 전화번호

        Raises:
            401: 유저를 없거나, 활성화 상태가 아니거나, 탈퇴한 경우
            403: 사장님이 아닌 경우
        """
        user_data = self.OutputSerializer(request.user).data
        return create_response(data=user_data, status_code=status.HTTP_200_OK)


class UserProfileUpdateAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        name = serializers.CharField(required=True, max_length=32)
        email = serializers.EmailField(required=True, max_length=256)

    class OutputSerializer(BaseSerializer):
        name = serializers.CharField()
        email = serializers.EmailField()
        phone_number = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_service = UserContainer.user_service()

    def patch(self, request: Request) -> Response:
        """유저가 자신의 정보를 수정합니다.
        url: /partner/api/v1/users/profile

        Args:
            name (str): 이름
            email (str): 이메일

        Returns:
            OutSerializer: 유저 정보
                name (str): 이름
                email (str): 이메일
                phone_number (str): 전화번호

        Raises:
            400: 이메일이 중복되는 경우, 요청 데이터가 잘못된 경우
            401: 유저를 없거나, 활성화 상태가 아니거나, 탈퇴한 경우
            403: 사장님이 아닌 경우
        """
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        user = self._user_service.update_user(user=request.user, data=input_serializer.validated_data)

        user_data = self.OutputSerializer(user).data
        return create_response(data=user_data, status_code=status.HTTP_200_OK)
