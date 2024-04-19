from collections import OrderedDict

import pytest

from mung_manager.common.exception.exceptions import ValidationException
from mung_manager.users.services.users import UserService

pytestmark = pytest.mark.django_db


class TestUpdateUser:
    """
    UserService의 update_user 테스트 클래스

    - Test List:
        Success:
            - update_user_success
        Fail:
            - update_user_fail_duplicate_email
    """

    def setup_method(self):
        self.user_service = UserService()

    def test_update_user_success(self, active_partner_user):
        """유저 정보 수정 성공 테스트

        Args:
            active_partner_user : 활성화된 사장님 유저
        """
        user_data = OrderedDict(
            email="test@test.com",
            name="test",
        )

        user = self.user_service.update_user(user=active_partner_user, data=user_data)

        assert user.email == user_data["email"]
        assert user.name == user_data["name"]

    def test_update_user_fail_duplicate_email(self, active_partner_user, active_guest_user):
        """유저 정보 수정 실패 테스트 (중복된 이메일)

        Args:
            active_partner_user : 활성화된 사장님 유저
            active_guest_user : 활성화된 손님 유저
        """
        user_data = OrderedDict(
            email=active_guest_user.email,
            name="test",
        )

        with pytest.raises(ValidationException) as e:
            self.user_service.update_user(user=active_partner_user, data=user_data)

        assert str(e.value) == "Email already exists."
        assert isinstance(e.value, ValidationException)
