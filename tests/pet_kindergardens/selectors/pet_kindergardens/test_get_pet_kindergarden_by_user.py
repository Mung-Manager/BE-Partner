import pytest

from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)

pytestmark = pytest.mark.django_db


class TestGetPetKindergardenByUser:
    """
    PetKindergardenSelector의 get_pet_kindergarden_by_user 테스트 클래스

    - Test List:
        Success:
            - get_pet_kindergarden_by_user_success
        Fail:
            - get_pet_kindergarden_by_user_fail_does_not_exist
    """

    def setup_method(self):
        self.pet_kindergarden_selector = PetKindergardenSelector()

    def test_get_pet_kindergarden_by_user_success(self, pet_kindergarden):
        """소셜 아이디로 유저 조회 성공 테스트

        Args:
            pet_kindergarden : 반려동물 유치원
        """
        pet_kindergarden_data = self.pet_kindergarden_selector.get_pet_kindergarden_by_user(pet_kindergarden.user)
        assert pet_kindergarden_data == pet_kindergarden

    def test_get_pet_kindergarden_by_user_fail_does_not_exist(self):
        """소셜 아이디로 유저 조회 실패 테스트 (존재하지 않는 유저)"""
        pet_kindergarden = self.pet_kindergarden_selector.get_pet_kindergarden_by_user(None)
        assert pet_kindergarden is None
