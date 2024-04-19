from typing import Optional

from mung_manager.users.models import User
from mung_manager.users.selectors.abstracts import AbstractUserSelector


class UserSelector(AbstractUserSelector):
    """이 클래스는 유저를 데이터베이스에서 PULL하는 역할을 담당합니다."""

    def get_user_by_social_id(self, social_id: str) -> Optional[User]:
        """이 함수는 소셜 아이디로 유저를 조회합니다.

        Args:
            social_id (str): 소셜 아이디

        Returns:
            Optional[User]: 유저 객체
        """
        try:
            return User.objects.filter(social_id=social_id).get()
        except User.DoesNotExist:
            return None

    def check_is_exists_user_by_email_excluding_self(self, user, email: Optional[str] = None) -> bool:
        """이 함수는 이메일로 자신을 제외한 유저를 조회합니다.

        Args:
            email (Optional[str]): 이메일
            user (User): 유저 객체

        Returns:
            bool: 유저 존재 여부
        """
        return User.objects.filter(email=email).exclude(id=user.id).exists()
