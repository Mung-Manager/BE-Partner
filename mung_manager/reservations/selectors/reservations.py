from typing import List

from django.db.models import Q

from mung_manager.reservations.enums import ReservationStatus
from mung_manager.reservations.models import Reservation
from mung_manager.reservations.selectors.abstracts import AbstractReservationSelector


class ReservationSelector(AbstractReservationSelector):
    def check_is_exists_unpending_reservation_by_customer_id_and_customer_pet_id(
        self, customer_id: int, customer_pet_id: int
    ) -> bool:
        """고객 아이디와 고객 반려동물 아이디로 대기 중이 아닌 예약이 존재하는지 확인합니다.

        Args:
            customer_id (int): 고객 아이디
            customer_pet_id (int): 고객 반려동물 아이디

        Returns:
            bool: 대기 중이 아닌 예약이 존재하면 True, 아니면 False를 반환
        """
        return Reservation.objects.filter(
            Q(customer_id=customer_id)
            & Q(customer_pet_id=customer_pet_id)
            & ~Q(reservation_status=ReservationStatus.PENDING.value)
        ).exists()

    def check_is_exists_pending_reservation_by_customer_id_and_customer_pet_ids(
        self, customer_id: int, customer_pet_ids: List[int]
    ) -> bool:
        """고객 아이디와 고객 반려동물 아이디로 대기 중인 예약이 존재하는지 확인합니다.

        Args:
            customer_id (int): 고객 아이디
            customer_pet_ids (int): 고객 반려동물 아이디

        Returns:
            bool: 대기 중인 예약이 존재하면 True, 아니면 False를 반환
        """
        return Reservation.objects.filter(
            customer_id=customer_id,
            customer_pet_id__in=customer_pet_ids,
            reservation_status=ReservationStatus.PENDING.value,
        ).exists()
