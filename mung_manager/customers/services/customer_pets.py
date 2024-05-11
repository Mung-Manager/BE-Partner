from django.db import transaction

from mung_manager.common.constants import SYSTEM_CODE
from mung_manager.common.selectors import check_object_or_not_found
from mung_manager.customers.selectors.customers import CustomerSelector
from mung_manager.customers.services.abstracts import AbstractCustomerPetService
from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)
from mung_manager.reservations.selectors.reservations import ReservationSelector


class CustomerPetService(AbstractCustomerPetService):
    """이 클래스는 고객 반려동물을 DB에서 PUSH하는 비즈니스 로직을 담당합니다."""

    def __init__(
        self,
        customer_selector: CustomerSelector,
        pet_kindergarden_selector: PetKindergardenSelector,
        reservation_selector: ReservationSelector,
    ):
        self._customer_selector = customer_selector
        self._pet_kindergarden_selector = pet_kindergarden_selector
        self._reservation_selector = reservation_selector

    @transaction.atomic
    def check_is_possible_delete_customer_pet(
        self,
        user,
        pet_kindergarden_id: int,
        customer_id: int,
        customer_pet_id: int,
    ) -> bool:
        """이 함수는 고객의 반려동물 삭제가 가능한지 확인합니다.

        Args:
            user: 유저 객체
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            customer_id (int): 고객 아이디
            customer_pet_id (int): 고객 반려동물 아이디

        Returns:
            bool: 반려동물 삭제 가능 여부 (True: 가능, False: 불가능)
        """
        check_object_or_not_found(
            self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
                pet_kindergarten_id=pet_kindergarden_id,
                user=user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )
        is_exists = self._reservation_selector.check_is_exists_unpending_reservation_by_customer_id_and_customer_pet_id(
            customer_id=customer_id, customer_pet_id=customer_pet_id
        )
        return is_exists
