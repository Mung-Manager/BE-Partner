import pytest

from mung_manager.users.enums import UserProvider
from mung_manager.users.services.users import UserService

pytestmark = pytest.mark.django_db


class TestCreateSocialUser:
    """
    UserService의 create_social_user 테스트 클래스

    - Test List:
        Success:
            - create_social_user_success
            - create_social_user_success_already_exist
    """

    def setup_method(self):
        self.user_service = UserService()

    def test_create_social_user_success(self, user_social_provider, group):
        """소셜 유저 생성 성공 테스트 (새로운 유저)

        Args:
            user_social_provider : 유저 제공자
            group : 권한 그룹
        """
        email = "test@test.com"
        name = "test"
        social_id = "test_id"
        phone_number = "010-1234-1234"
        birth = "1999-01-01"
        gender = "M"
        social_provider = UserProvider.KAKAO.value

        user = self.user_service.create_social_user(
            email=email,
            name=name,
            social_id=social_id,
            phone_number=phone_number,
            birth=birth,
            gender=gender,
            social_provider=social_provider,
        )

        assert user.email == email
        assert user.name == name
        assert user.social_id == social_id
        assert user.phone_number == phone_number
        assert str(user.birth) == birth
        assert user.gender == gender
        assert user.user_social_provider_id == social_provider

    def test_create_social_user_success_already_exist(self, active_partner_user):
        """소셜 유저 생성 성공 테스트 (이미 존재하는 유저)

        Args:
            active_partner_user : 활성화된 사장님 유저
        """
        user = self.user_service.create_social_user(
            email=active_partner_user.email,
            name=active_partner_user.name,
            social_id=active_partner_user.social_id,
            phone_number=active_partner_user.phone_number,
            birth=active_partner_user.birth,
            gender=active_partner_user.gender,
            social_provider=active_partner_user.user_social_provider_id,
        )

        assert user == active_partner_user

    def test_create_social_user_success_phone_number_update(self, active_partner_user):
        """소셜 유저 생성 성공 테스트 (이미 존재하는 유저, 전화번호 변경)

        Args:
            active_partner_user : 활성화된 사장님 유저
        """
        phone_number = "010-1234-1234"

        user = self.user_service.create_social_user(
            email=active_partner_user.email,
            name=active_partner_user.name,
            gender=active_partner_user.gender,
            social_id=active_partner_user.social_id,
            phone_number=phone_number,
            birth=active_partner_user.birth,
            social_provider=active_partner_user.user_social_provider_id,
        )

        active_partner_user.refresh_from_db()

        assert user == active_partner_user
        assert user.phone_number == phone_number
