import pytest

from mung_manager.pet_kindergardens.selectors.raw_pet_kindergardens import (
    RawPetKindergardenSelector,
)

pytestmark = pytest.mark.django_db


class TestGetRawPetKindergardenQuerySetByName:
    """
    RawPetKindergardenSelector의 get_raw_pet_kindergarden_queryset_by_name 테스트 클래스

    - Test List:
        Success:
            - get_raw_pet_kindergarden_queryset_by_name_success
    """

    def setup_method(self):
        self.raw_pet_kindergarden_selector = RawPetKindergardenSelector()

    def test_get_raw_pet_kindergarden_queryset_by_name_success(self, raw_pet_kindergarden):
        """이름으로 반려동물 유치원 조회 성공 테스트

        Args:
            raw_pet_kindergarden : 반려동물 유치원
        """
        raw_pet_kindergarden_queryset = self.raw_pet_kindergarden_selector.get_raw_pet_kindergarden_queryset_by_name(
            raw_pet_kindergarden.name
        )
        assert raw_pet_kindergarden_queryset[0] == raw_pet_kindergarden
