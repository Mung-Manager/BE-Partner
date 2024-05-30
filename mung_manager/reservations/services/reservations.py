from django.db import transaction

from mung_manager.common.constants import SYSTEM_CODE
from mung_manager.common.selectors import (
    check_object_or_not_found,
    get_object_or_not_found,
)
from mung_manager.common.services import update_model
from mung_manager.pet_kindergardens.selectors.pet_kindergardens import (
    PetKindergardenSelector,
)
from mung_manager.reservations.models import Reservation
from mung_manager.reservations.selectors.reservations import ReservationSelector
from mung_manager.reservations.services.abstracts import AbstractReservationService


class ReservationService(AbstractReservationService):
    """이 클래스는 예약을 DB에 PUSH하는 비즈니스 로직을 담당합니다."""

    def __init__(
        self,
        pet_kindergarden_selector: PetKindergardenSelector,
        reservation_selector: ReservationSelector,
    ):
        self._pet_kindergarden_selector = pet_kindergarden_selector
        self._reservation_selector = reservation_selector

    @transaction.atomic
    def toggle_reservation_is_attended(self, pet_kindergarden_id: int, reservation_id: int, user) -> Reservation:
        """이 함수는 예약의 출석 활성화/비활성화를 변경합니다.

        Args:
            pet_kindergarden_id (int): 반려동물 유치원 아이디
            reservation_id (int): 예약 아이디
            user: 유저 객체

        Returns:
            Reservation: 예약 객체
        """
        check_object_or_not_found(
            self._pet_kindergarden_selector.check_is_exists_pet_kindergarden_by_id_and_user(
                pet_kindergarden_id=pet_kindergarden_id,
                user=user,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_PET_KINDERGARDEN"),
            code=SYSTEM_CODE.code("NOT_FOUND_PET_KINDERGARDEN"),
        )

        reservation = get_object_or_not_found(
            self._reservation_selector.get_reservation_by_id(
                reservation_id=reservation_id,
            ),
            msg=SYSTEM_CODE.message("NOT_FOUND_RESERVATION"),
            code=SYSTEM_CODE.code("NOT_FOUND_RESERVATION"),
        )

        data = {
            "is_attended": not reservation.is_attended,
        }
        reservation, has_updated = update_model(
            instance=reservation,
            data=data,
            fields=list(data.keys()),
        )
        return reservation
