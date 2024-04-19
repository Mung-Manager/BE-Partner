import pytest
from django.contrib.auth.hashers import check_password

from mung_manager.users.enums import AuthGroup, UserProvider
from mung_manager.users.models import User

pytestmark = pytest.mark.django_db


class TestCreateAdmin:
    """
    UserManager의 create_admin 테스트 클래스

    - Test List:
        Success:
            - create_admin_success
    """

    def test_create_admin_success(self, user_social_provider, group):
        """어드민 유저 생성 성공 테스트

        Args:
            user_social_provider : 유저 제공자
            group : 권한 그룹
        """
        email = "test@test.com"
        name = "테스트"
        phone_number = "010-0000-0000"
        password = "test1234"
        birth = "1990-01-01"

        user = User.objects.create_admin(
            email=email,
            name=name,
            phone_number=phone_number,
            password=password,
            birth=birth,
        )

        assert user.email == email
        assert user.name == name
        assert user.phone_number == phone_number
        assert check_password(password, user.password)
        assert str(user.birth) == birth
        assert user.user_social_provider_id == UserProvider.EMAIL.value
        assert user.groups.first().id == AuthGroup.ADMIN.value
