from typing import Optional

from mung_manager.common.exception.exceptions import NotFoundException
from mung_manager.pet_kindergardens.models import PetKindergarden
from mung_manager.pet_kindergardens.selectors.abstracts import (
    AbstractPetKindergardenSelector,
)


class PetKindergardenSelector(AbstractPetKindergardenSelector):
    """
    이 클래스는 반려동물 유치원을 SELECT, EXISTS를 위한 클래스입니다.
    """

    def check_is_exists_pet_kindergarden_by_user(self, user) -> bool:
        """
        이 함수는 유저로 반려동물 유치원이 존재하는지 확인합니다.

        Args:
            user: User: 유저 객체

        Returns:
            bool: 반려동물 유치원이 존재하면 True를 반환하며 존재하지 않으면 False를 반환
        """
        return PetKindergarden.objects.filter(user=user).exists()

    def get_pet_kindergarden_by_user(self, user) -> Optional[PetKindergarden]:
        """
        이 함수는 유저로 반려동물 유치원을 조회합니다.

        Args:
            user: User: 유저 객체

        Returns:
            Optional[PetKindergarden]: 반려동물 유치원 객체이며 존재하지 않으면 None을 반환
        """
        try:
            return PetKindergarden.objects.filter(user=user).get()
        except PetKindergarden.DoesNotExist:
            return None

    def check_is_exists_pet_kindergarden_by_id_and_user(self, pet_kindergarten_id: int, user) -> bool:
        """
        이 함수는 반려동물 유치원 아이디와 유저로 반려동물 유치원이 존재하는지 확인합니다.

        Args:
            pet_kindergarten_id (int): 반려동물 유치원 아이디
            user: User: 유저 객체

        Returns:
            bool: 반려동물 유치원이 존재하면 True를 반환하며 존재하지 않으면 예외를 발생시킵니다.
        """
        is_exists = PetKindergarden.objects.filter(id=pet_kindergarten_id, user=user).exists()

        if is_exists is False:
            raise NotFoundException(detail="PetKindergarden does not exist.", code="not_found_pet_kindergarden")

        return is_exists
