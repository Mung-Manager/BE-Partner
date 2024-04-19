import pytest

from mung_manager.users.enums import AuthGroup, UserProvider
from mung_manager.users.models import User

pytestmark = pytest.mark.django_db


class TestCreateSocialUser:
    """
    UserManager의 create_social_user 테스트 클래스

    - Test List:
        Success:
            - create_social_user_success
    """

    def test_create_social_user_success(self, user_social_provider, group):
        """소셜 유저 생성 성공 테스트

        Args:
            user_social_provider : 유저 제공자
            group : 권한 그룹
        """
        email = "test@test.com"
        name = "테스트"
        social_id = "test_id"
        phone_number = "010-0000-0000"
        birth = "1990-01-01"
        social_provider = UserProvider.KAKAO.value

        user = User.objects.create_social_user(
            email=email,
            name=name,
            social_id=social_id,
            phone_number=phone_number,
            birth=birth,
            social_provider=social_provider,
        )

        assert user.email == email
        assert user.name == name
        assert user.social_id == social_id
        assert user.phone_number == phone_number
        assert user.has_usable_password() is False
        assert str(user.birth) == birth
        assert user.user_social_provider_id == UserProvider.KAKAO.value
        assert user.groups.first().id == AuthGroup.PARTNER.value
