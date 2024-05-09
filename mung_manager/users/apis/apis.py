from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from mung_manager.apis.mixins import APIAuthMixin
from mung_manager.common.base.serializers import BaseSerializer
from mung_manager.users.containers import UserContainer


class UserProfileDetailAPI(APIAuthMixin, APIView):
    class OutputSerializer(BaseSerializer):
        name = serializers.CharField(label="유저 이름")
        email = serializers.EmailField(label="유저 이메일")
        phone_number = serializers.CharField(label="유저 전화번호")

    def get(self, request: Request) -> Response:
        user_data = self.OutputSerializer(request.user).data
        return Response(data=user_data, status=status.HTTP_200_OK)


class UserProfileUpdateAPI(APIAuthMixin, APIView):
    class InputSerializer(BaseSerializer):
        name = serializers.CharField(required=True, max_length=32, label="유저 이름")
        email = serializers.EmailField(required=True, max_length=256, label="유저 이메일")

    class OutputSerializer(BaseSerializer):
        name = serializers.CharField(label="유저 이름")
        email = serializers.EmailField(label="유저 이메일")
        phone_number = serializers.CharField(label="유저 전화번호")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_service = UserContainer.user_service()

    def patch(self, request: Request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        user = self._user_service.update_user(
            user=request.user, data=input_serializer.validated_data
        )

        user_data = self.OutputSerializer(user).data
        return Response(data=user_data, status=status.HTTP_200_OK)
