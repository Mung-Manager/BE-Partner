from django.contrib.auth.models import Group

from mung_manager.users.selectors.abstracts import AbstractGroupSelector


class GroupSelector(AbstractGroupSelector):
    """이 클래스는 그룹을 DB에 PULL하는 비즈니스 로직을 담당합니다."""

    def exists_by_id_and_user(self, group_id: int, user) -> bool:
        """이 함수는 그룹 ID와 유저를 받아 그룹이 존재하는지 확인합니다.

        Args:
            group_id (int): 그룹 ID
            user: 유저 객체

        Returns:
            bool: 그룹 존재 여부
        """
        return Group.objects.filter(id=group_id, user=user).exists()
